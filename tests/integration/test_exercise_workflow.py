import pytest
from datetime import date

from app.modules.diaries.service import DiaryService
from app.modules.exersices_catalog.service import ExerciseService
from app.modules.exersices_catalog.schemas import CreateExerciseIn
from app.modules.users.dao import UserDAO
from app.modules.diaries.dao import DiaryDAO


@pytest.mark.integration
class TestExerciseIntegration:
    """Интеграционные тесты для работы с упражнениями"""
    
    async def test_exercise_workflow(self, database_session):
        """Создание упражнения → добавление в день"""
        # 1. Создаём пользователя и дневник
        user = await UserDAO.add(
            database_session,
            telegram_id=555666777,
            username="sport_user", 
            first_name="Sport User"
        )
        await database_session.flush()
        
        # Проверяем пользователя
        assert user.id is not None
        assert user.username == "sport_user"
        
        diary = await DiaryDAO.add(database_session, id=user.id)
        await database_session.flush()
        
        # Проверяем дневник
        assert diary.id == user.id
        
        # 2. Создаём упражнение в каталоге
        exercise_service = ExerciseService(session=database_session)
        await exercise_service.add_product(
            CreateExerciseIn(
                title="Бег",
                kcal_30m=300
            )
        )
        
        # 3. Добавляем упражнение в день
        diary_service = DiaryService(session=database_session)
        await diary_service.add_exercise_to_day(
            user_id=user.id,
            diary_id=diary.id, 
            target_date=date(2025, 1, 1),
            exercise_id=1,  # ID созданного упражнения
            minutes=45.0
        )
        
        # 4. Проверяем через получение дня
        day = await diary_service.get_by_date(
            user_id=user.id,
            diary_id=diary.id,
            target_date=date(2025, 1, 1)
        )
        
        # Проверяем что день создался правильно
        assert day is not None
        assert day.user_id == user.id
        assert day.diary_id == diary.id
        assert day.date == date(2025, 1, 1)