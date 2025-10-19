import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.modules.exersices_catalog.service import ExerciseService


class TestExerciseService:
    """Тесты для ExerciseService"""

    @pytest_asyncio.fixture
    def mock_session(self):
        return AsyncMock()

    @pytest_asyncio.fixture
    def exercise_service(self, mock_session):
        return ExerciseService(session=mock_session)

    @pytest.fixture
    def exercise_data(self):
        # Мок вместо реальной схемы
        mock_payload = MagicMock()
        mock_payload.model_dump.return_value = {
            "title": "Бег", 
            "kcal_30m": 300
        }
        return mock_payload

    async def test_add_exercise_success(self, exercise_service, exercise_data):
        """Успешное добавление упражнения"""
        with patch('app.modules.exersices_catalog.service.ExersiceDAO.add', new_callable=AsyncMock) as mock_add:
            await exercise_service.add_product(exercise_data)

            mock_add.assert_called_once_with(
                exercise_service.session,
                title="Бег",
                kcal_30m=300
            )
            exercise_service.session.commit.assert_called_once()

    async def test_add_exercise_duplicate(self, exercise_service, exercise_data):
        """Ошибка при дубликате упражнения"""
        with patch('app.modules.exersices_catalog.service.ExersiceDAO.add', new_callable=AsyncMock) as mock_add:
            mock_add.side_effect = IntegrityError("test", "test", "test")

            with pytest.raises(HTTPException) as exc_info:
                await exercise_service.add_product(exercise_data)

            assert exc_info.value.status_code == status.HTTP_409_CONFLICT
            assert "Упражнение уже добавлено" in exc_info.value.detail
            exercise_service.session.rollback.assert_called_once()

    async def test_add_exercise_rollback_on_error(self, exercise_service, exercise_data):
        """Откат транзакции при любой ошибке"""
        with patch('app.modules.exersices_catalog.service.ExersiceDAO.add', new_callable=AsyncMock) as mock_add:
            mock_add.side_effect = Exception("Some error")

            with pytest.raises(Exception):
                await exercise_service.add_product(exercise_data)

            exercise_service.session.rollback.assert_called_once()

    async def test_list_exercises_success(self, exercise_service):
        """Успешное получение списка упражнений"""
        mock_exercises = [AsyncMock(), AsyncMock()]
        
        with patch('app.modules.exersices_catalog.service.ExersiceDAO.find_all', 
                  new_callable=AsyncMock, return_value=mock_exercises) as mock_find_all:

            result = await exercise_service.list_exercises()

            assert result == mock_exercises
            mock_find_all.assert_called_once_with(exercise_service.session)