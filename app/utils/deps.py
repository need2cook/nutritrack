from fastapi import Header, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.utils.tg_initdata import parse_and_verify_init_data, InitDataError
from app.db import db_sessions
from app.db import UserDAO
from app.db import User


async def verify_and_set_initdata(
    request: Request,
    x_telegram_init_data: str = Header(alias="X-Telegram-Init-Data"),
):
    try:
        request.state.init = parse_and_verify_init_data(
            x_telegram_init_data, settings.BOT_TOKEN
        )
    except InitDataError as e:
        raise HTTPException(status_code=401, detail=str(e))


async def get_current_user_readonly(
    request: Request,
    session: AsyncSession = Depends(db_sessions.get_db),
) -> User:
    cached = getattr(request.state, "user", None)
    if cached is not None:
        return cached

    init = getattr(request.state, "init", None)
    if not init:
        raise HTTPException(status_code=401, detail="No init data")

    tg = init["user"]
    user = await session.scalar(
        select(User).where(User.telegram_id == tg["id"])
    )
    if not user:
        raise HTTPException(status_code=401, detail="User not registered (run handshake)")
    
    request.state.user = user
    return user


async def ensure_user_via_upsert(
    request: Request,
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
) -> User:
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

