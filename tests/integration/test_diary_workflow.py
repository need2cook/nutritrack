import pytest
from datetime import date

from app.modules.diaries.service import DiaryService
from app.modules.users.dao import UserDAO
from app.modules.diaries.dao import DiaryDAO


@pytest.mark.integration
class TestDiaryIntegration:
    """Интеграционные тесты для дневника"""
    
    async def test_create_user_and_diary_workflow(self, database_session):
        """Создание пользователя → создание дневника → создание дня"""
        # 1. Создаём пользователя
        user = await UserDAO.add(
            database_session,
            telegram_id=123456789,
            username="test_user",
            first_name="Test User"
        )
        await database_session.flush()
        
        # Проверяем что пользователь создался
        assert user.id is not None
        assert user.telegram_id == 123456789
        
        # 2. Создаём дневник
        diary = await DiaryDAO.add(
            database_session,
            id=user.id
        )
        await database_session.flush()
        
        # Проверяем что дневник создался
        assert diary.id == user.id
        
        # 3. Создаём день через сервис
        diary_service = DiaryService(session=database_session)
        day = await diary_service.get_or_create_day(
            user_id=user.id,
            diary_id=diary.id,
            target_date=date(2025, 1, 1)
        )
        
        # Проверяем
        assert day.user_id == user.id
        assert day.diary_id == diary.id
        assert day.date == date(2025, 1, 1)
        
        # Проверяем переиспользование дня
        same_day = await diary_service.get_or_create_day(
            user_id=user.id,
            diary_id=diary.id, 
            target_date=date(2025, 1, 1)
        )
        assert same_day.id == day.id

    async def test_empty_database_initially(self, database_session):
        """Проверяем что БД чистая перед каждым тестом"""
        users = await UserDAO.find_all(database_session)
        assert users == []  # В начале теста БД пустая

    async def test_transaction_rollback(self, database_session):
        """Проверяем что транзакции откатываются после теста"""
        # Создаём пользователя в этом тесте
        user = await UserDAO.add(
            database_session,
            telegram_id=999888777,
            username="temp_user", 
            first_name="Temp User"
        )
        await database_session.flush()
        
        # Проверяем что пользователь создался
        assert user.id is not None
        assert user.username == "temp_user"
        
        # Проверяем что пользователь находится в БД
        found_user = await UserDAO.find_one_or_none(
            database_session, 
            telegram_id=999888777
        )
        assert found_user is not None
        assert found_user.username == "temp_user"
        assert found_user.id == user.id 