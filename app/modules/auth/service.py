from fastapi import Header, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hmac, hashlib, json, time
from urllib.parse import parse_qsl, unquote

from app.core.config import settings
from app.core.sessionmaker_fastapi import db_sessions
from app.modules.users import UserDAO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.users.models import User

class InitDataError(Exception): ...


class AuthService:

    @staticmethod
    async def ensure_user_via_upsert(
        request: Request,
        session: AsyncSession = Depends(db_sessions.get_db_with_commit),
    ) -> "User":
        """
        Делает upsert и возвращает пользователя.
        Использовать ТОЛЬКО в /api/auth/handshake.
        """
        cached = getattr(request.state, "user", None)
        if cached is not None:
            return cached

        init = getattr(request.state, "init", None)
        if not init:
            raise HTTPException(status_code=401, detail="No init data")

        u = init["user"]
        user, _created = await UserDAO.upsert_user(
            session=session,
            unique_fields=["telegram_id"],
            telegram_id=u["id"],
            username=u.get("username"),
            first_name=u.get("first_name") or "",
        )
        request.state.user = user
        return user
    
    @staticmethod
    def parse_and_verify_init_data(init_data: str, bot_token: str, *, max_age_sec: int = 3600000) -> dict:
        if not init_data:
            raise InitDataError("Empty initData")
        
        data = dict(parse_qsl(unquote(init_data)))
        
        if 'hash' not in data:
            raise InitDataError("Missing hash")
        
        received_hash = data.pop('hash')
        
        data_check_string = '\n'.join([f"{k}={v}" for k, v in sorted(data.items())])
        
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(calculated_hash, received_hash):
            raise InitDataError("Invalid hash initData")
        
        try:
            auth_date = int(data.get("auth_date", "0"))
        except ValueError:
            raise InitDataError("Bad 'auth_date'")
        if auth_date == 0 or (time.time() - auth_date) > max_age_sec:
            raise InitDataError("initData expired")
        
        for k in ("user", "chat", "receiver"):
            if k in data:
                data[k] = json.loads(data[k])
        return data

    @staticmethod
    async def verify_and_set_initdata(
        request: Request,
        x_telegram_init_data: str = Header(alias="X-Telegram-Init-Data"),
    ):
        try:
            request.state.init = AuthService.parse_and_verify_init_data(
                x_telegram_init_data, settings.BOT_TOKEN
            )
        except InitDataError as e:
            raise HTTPException(status_code=401, detail=str(e))

    @staticmethod
    async def get_current_user_readonly(
        request: Request,
        session: AsyncSession = Depends(db_sessions.get_db),
    ) -> "User":
        cached = getattr(request.state, "user", None)
        if cached is not None:
            return cached

        init = getattr(request.state, "init", None)
        if not init:
            raise HTTPException(status_code=401, detail="No init data")

        tg = init["user"]

        user = await UserDAO.find_one_or_none(session, telegram_id=tg["id"])
        if not user:
            raise HTTPException(status_code=401, detail="User not registered (run handshake)")
        
        request.state.user = user
        return user


