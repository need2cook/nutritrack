import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException, status

from app.modules.users.service import UserService


class TestUserService:
    """Тесты для UserService"""

    @pytest_asyncio.fixture
    def mock_session(self):
        return AsyncMock()

    @pytest_asyncio.fixture
    def user_service(self, mock_session):
        return UserService(session=mock_session)

    @pytest.fixture
    def mock_user(self):
        user = MagicMock()
        user.id = 1
        user.telegram_id = 123456789
        user.username = "test_user"
        user.first_name = "Test"
        user.current_weight = 70.5
        return user

    # ТЕСТЫ ПОЛУЧЕНИЯ ПРОФИЛЯ
    async def test_get_profile_success(self, user_service, mock_user):
        """Успешное получение профиля пользователя"""
        with patch('app.modules.users.service.UserDAO.find_one_or_none_by_id', 
                  new_callable=AsyncMock, return_value=mock_user) as mock_find:

            result = await user_service.get_profile(user_id=1)

            assert result == mock_user
            mock_find.assert_called_once_with(user_service.session, data_id=1)

    async def test_get_profile_not_found(self, user_service):
        """Пользователь не найден"""
        with patch('app.modules.users.service.UserDAO.find_one_or_none_by_id', 
                  new_callable=AsyncMock, return_value=None) as mock_find:

            result = await user_service.get_profile(user_id=999)

            assert result is None
            mock_find.assert_called_once_with(user_service.session, data_id=999)

    # ТЕСТЫ ИЗМЕНЕНИЯ ВЕСА
    async def test_edit_weight_success(self, user_service):
        """Успешное изменение веса пользователя"""
        with patch('app.modules.users.service.UserDAO.update', new_callable=AsyncMock) as mock_update:
            await user_service.edit_weight(user_id=1, new_weight=75.0)

            mock_update.assert_called_once_with(
                user_service.session,
                {'id': 1},
                current_weight=75.0
            )
            user_service.session.commit.assert_called_once()

    async def test_edit_weight_database_error(self, user_service):
        """Ошибка базы данных при изменении веса"""
        with patch('app.modules.users.service.UserDAO.update', new_callable=AsyncMock) as mock_update:
            mock_update.side_effect = Exception("Database connection failed")

            with pytest.raises(HTTPException) as exc_info:
                await user_service.edit_weight(user_id=1, new_weight=75.0)

            assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Что-то пошло не так" in exc_info.value.detail
            user_service.session.rollback.assert_called_once()

    async def test_edit_weight_rollback_on_error(self, user_service):
        """Проверка отката транзакции при ошибке"""
        with patch('app.modules.users.service.UserDAO.update', new_callable=AsyncMock) as mock_update:
            mock_update.side_effect = Exception("Some error")

            with pytest.raises(HTTPException):
                await user_service.edit_weight(user_id=1, new_weight=75.0)

            user_service.session.rollback.assert_called_once()
            user_service.session.commit.assert_not_called()