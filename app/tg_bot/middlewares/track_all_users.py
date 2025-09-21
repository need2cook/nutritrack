from typing import Callable, Awaitable, Dict, Any, cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from cachetools import TTLCache

from app.db import UserDAO
from app.db import async_session_maker


class TrackAllUsersMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.cache = TTLCache(
            maxsize=1000,
            ttl=60 * 60 * 6,  # 6 часов
        )

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # Говорим IDE, что event на самом деле – Message
        event = cast(Message, event)
        user_id = event.from_user.id

        # Надо обновить данные пользователя, если он не в кэше
        if user_id not in self.cache:
            async with async_session_maker() as session:
                try:
                    await UserDAO.upsert_user(
                        session=session,
                        unique_fields=['telegram_id'],
                        telegram_id=event.from_user.id,
                        first_name=event.from_user.first_name,
                        username=event.from_user.username
                    )
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise
            self.cache[user_id] = None
        return await handler(event, data)
