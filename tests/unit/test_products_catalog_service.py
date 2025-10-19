import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.modules.products_catalog.service import ProductService


class TestProductService:
    """Тесты для ProductService"""

    @pytest_asyncio.fixture
    def mock_session(self):
        return AsyncMock()

    @pytest_asyncio.fixture
    def product_service(self, mock_session):
        return ProductService(session=mock_session)

    @pytest.fixture
    def product_data(self):
        # Мок вместо реальной схемы
        mock_payload = MagicMock()
        mock_payload.model_dump.return_value = {
            "title": "Яблоко",
            "carbs_100g": 14.0,
            "proteins_100g": 0.3,
            "fats_100g": 0.2,
            "kcal_100g": 52
        }
        return mock_payload

    async def test_add_product_success(self, product_service, product_data):
        """Успешное добавление продукта"""
        with patch('app.modules.products_catalog.service.ProductDAO.add', new_callable=AsyncMock) as mock_add:
            await product_service.add_product(product_data)

            mock_add.assert_called_once_with(
                product_service.session,
                title="Яблоко",
                carbs_100g=14.0,
                proteins_100g=0.3,
                fats_100g=0.2,
                kcal_100g=52
            )
            product_service.session.commit.assert_called_once()

    async def test_add_product_duplicate(self, product_service, product_data):
        """Ошибка при дубликате продукта"""
        with patch('app.modules.products_catalog.service.ProductDAO.add', new_callable=AsyncMock) as mock_add:
            mock_add.side_effect = IntegrityError("test", "test", "test")

            with pytest.raises(HTTPException) as exc_info:
                await product_service.add_product(product_data)

            assert exc_info.value.status_code == status.HTTP_409_CONFLICT
            assert "Продукт уже добавлен" in exc_info.value.detail
            product_service.session.rollback.assert_called_once()

    async def test_add_product_rollback_on_error(self, product_service, product_data):
        """Откат транзакции при любой ошибке"""
        with patch('app.modules.products_catalog.service.ProductDAO.add', new_callable=AsyncMock) as mock_add:
            mock_add.side_effect = Exception("DB error")

            with pytest.raises(Exception):
                await product_service.add_product(product_data)

            product_service.session.rollback.assert_called_once()

    async def test_list_products_success(self, product_service):
        """Успешное получение списка продуктов"""
        mock_products = [MagicMock(), MagicMock()]
        
        with patch('app.modules.products_catalog.service.ProductDAO.find_all', 
                  new_callable=AsyncMock, return_value=mock_products) as mock_find_all:

            result = await product_service.list_products()

            assert result == mock_products
            mock_find_all.assert_called_once_with(product_service.session)