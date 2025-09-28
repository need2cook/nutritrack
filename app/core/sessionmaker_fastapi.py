from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .db import async_session_maker
from loguru import logger


class DatabaseSession:
    @staticmethod
    async def get_session(commit: bool = False) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            try:
                yield session
                if commit:
                    await session.commit()
            except Exception as e:
                logger.error(f"Ошибка при работе с БД: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()

    @staticmethod
    async def get_db() -> AsyncGenerator[AsyncSession, None]:
        """Dependency для получения сессии без автоматического коммита"""
        async for session in DatabaseSession.get_session(commit=False):
            yield session

    @staticmethod
    async def get_db_with_commit() -> AsyncGenerator[AsyncSession, None]:
        """Dependency для получения сессии с автоматическим коммитом"""
        async for session in DatabaseSession.get_session(commit=True):
            yield session


db_sessions = DatabaseSession()
