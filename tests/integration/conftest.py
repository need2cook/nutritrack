import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.modules.base import Base


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Движок для тестовой БД (на всю сессию тестов)"""
    
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True
    )
    
    # Создаём все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # На всякий случай чистим
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Закрываем соединение после всех тестов
    await engine.dispose()


@pytest_asyncio.fixture
async def database_session(test_engine):
    """Сессия БД для каждого теста"""
    async_session = sessionmaker(
        test_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            yield session
        finally:
            # Откатываем изменения после каждого теста
            await session.rollback()