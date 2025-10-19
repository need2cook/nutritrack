import pytest
import pytest_asyncio
from datetime import date
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.modules.diaries.service import DiaryService


class TestDiaryService:
    """Тесты для DiaryService"""

    @pytest_asyncio.fixture
    def mock_session(self):
        return AsyncMock()

    @pytest_asyncio.fixture
    def diary_service(self, mock_session):
        return DiaryService(session=mock_session)

    @pytest.fixture
    def mock_day(self):
        day = MagicMock()
        day.id = 1
        day.date = date(2024, 1, 1)
        return day

    # ОСНОВНЫЕ СЦЕНАРИИ GET_OR_CREATE_DAY
    async def test_get_or_create_day_existing(self, diary_service, mock_day):
        """Получение существующего дня"""
        with patch('app.modules.diaries.service.DayDAO.find_one_or_none', 
                  new_callable=AsyncMock, return_value=mock_day) as mock_find:

            result = await diary_service.get_or_create_day(
                user_id=1, diary_id=1, target_date=date(2024, 1, 1)
            )

            assert result == mock_day
            mock_find.assert_called_once_with(diary_service.session, date=date(2024, 1, 1), user_id=1)

    async def test_get_or_create_day_new(self, diary_service, mock_day):
        """Создание нового дня"""
        with patch('app.modules.diaries.service.DayDAO.find_one_or_none', 
                  new_callable=AsyncMock, side_effect=[None, mock_day]), \
             patch('app.modules.diaries.service.DayDAO.add', new_callable=AsyncMock) as mock_add:

            result = await diary_service.get_or_create_day(
                user_id=1, diary_id=1, target_date=date(2024, 1, 1)
            )

            assert result == mock_day
            mock_add.assert_called_once_with(
                diary_service.session, diary_id=1, user_id=1, date=date(2024, 1, 1)
            )
            diary_service.session.flush.assert_called_once()

    async def test_get_or_create_day_integrity_error(self, diary_service):
        """Ошибка дубликата при создании дня"""
        with patch('app.modules.diaries.service.DayDAO.find_one_or_none', 
                  new_callable=AsyncMock, return_value=None), \
             patch('app.modules.diaries.service.DayDAO.add', 
                  new_callable=AsyncMock, side_effect=IntegrityError("test", "test", "test")):

            with pytest.raises(HTTPException) as exc_info:
                await diary_service.get_or_create_day(
                    user_id=1, diary_id=1, target_date=date(2024, 1, 1)
                )

            assert exc_info.value.status_code == status.HTTP_409_CONFLICT
            diary_service.session.rollback.assert_called_once()

    # ОСНОВНЫЕ СЦЕНАРИИ ПОЛУЧЕНИЯ ДНЕЙ
    async def test_get_today_success(self, diary_service, mock_day):
        """Успешное получение сегодняшнего дня"""
        with patch.object(diary_service, '_today', return_value=date(2024, 1, 1)), \
             patch.object(diary_service, 'get_or_create_day', 
                         new_callable=AsyncMock, return_value=mock_day):

            result = await diary_service.get_today(user_id=1, diary_id=1)

            assert result == mock_day
            diary_service.session.commit.assert_called_once()

    async def test_get_by_date_success(self, diary_service, mock_day):
        """Успешное получение дня по дате"""
        with patch.object(diary_service, 'get_or_create_day', 
                         new_callable=AsyncMock, return_value=mock_day):

            result = await diary_service.get_by_date(
                user_id=1, diary_id=1, target_date=date(2024, 1, 1)
            )

            assert result == mock_day
            diary_service.session.commit.assert_called_once()

    # ОСНОВНЫЕ СЦЕНАРИИ ДОБАВЛЕНИЯ/УДАЛЕНИЯ
    async def test_add_product_to_day_success(self, diary_service, mock_day):
        """Успешное добавление продукта в день"""
        with patch.object(diary_service, 'get_or_create_day', 
                         new_callable=AsyncMock, return_value=mock_day), \
             patch('app.modules.diaries.service.DayDAO.add_product', new_callable=AsyncMock):

            await diary_service.add_product_to_day(
                user_id=1, diary_id=1, target_date=date(2024, 1, 1),
                product_id=1, grams=100.0
            )

            diary_service.session.commit.assert_called_once()

    async def test_rm_product_from_day_success(self, diary_service, mock_day):
        """Успешное удаление продукта из дня"""
        with patch.object(diary_service, 'get_or_create_day', 
                         new_callable=AsyncMock, return_value=mock_day), \
             patch('app.modules.diaries.service.ProductEntityDAO.delete', 
                  new_callable=AsyncMock, return_value=True):

            await diary_service.rm_product_from_day(
                user_id=1, diary_id=1, target_date=date(2024, 1, 1), entry_id=1
            )

            diary_service.session.commit.assert_called_once()

    async def test_rm_product_from_day_not_found(self, diary_service, mock_day):
        """Продукт не найден при удалении"""
        with patch.object(diary_service, 'get_or_create_day', 
                         new_callable=AsyncMock, return_value=mock_day), \
             patch('app.modules.diaries.service.ProductEntityDAO.delete', 
                  new_callable=AsyncMock, return_value=False):

            with pytest.raises(HTTPException) as exc_info:
                await diary_service.rm_product_from_day(
                    user_id=1, diary_id=1, target_date=date(2024, 1, 1), entry_id=1
                )

            assert exc_info.value.status_code == status.HTTP_409_CONFLICT
            diary_service.session.rollback.assert_called_once()