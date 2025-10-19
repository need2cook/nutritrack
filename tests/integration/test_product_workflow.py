import pytest
from datetime import date

from app.modules.diaries.service import DiaryService
from app.modules.products_catalog.service import ProductService
from app.modules.products_catalog.schemas import CreateProductIn
from app.modules.users.dao import UserDAO
from app.modules.diaries.dao import DiaryDAO


@pytest.mark.integration
class TestProductIntegration:
    """Интеграционные тесты для работы с продуктами"""
    
    async def test_full_product_workflow(self, database_session):
        """Полный цикл: пользователь → продукт → добавление в день"""
        # 1. Создаём пользователя и дневник
        user = await UserDAO.add(
            database_session,
            telegram_id=111222333,
            username="food_user",
            first_name="Food User"
        )
        await database_session.flush()
        
        # Проверяем пользователя
        assert user.id is not None
        assert user.username == "food_user"
        
        diary = await DiaryDAO.add(database_session, id=user.id)
        await database_session.flush()
        
        # Проверяем дневник
        assert diary.id == user.id
        
        # 2. Создаём продукт в каталоге
        product_service = ProductService(session=database_session)
        await product_service.add_product(
            CreateProductIn(
                title="Банан",
                carbs_100g=22.8,
                proteins_100g=1.1,
                fats_100g=0.3,
                kcal_100g=89
            )
        )
        
        # 3. Создаём день и добавляем продукт
        diary_service = DiaryService(session=database_session)
        await diary_service.add_product_to_day(
            user_id=user.id,
            diary_id=diary.id,
            target_date=date(2025, 1, 1),
            product_id=1,  # ID созданного продукта
            grams=150.0
        )
        
        # 4. Проверяем что день создался с продуктом
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

    async def test_product_catalog_operations(self, database_session):
        """Операции с каталогом продуктов"""
        product_service = ProductService(session=database_session)
        
        unique_apple = "Тестовое яблоко 999"
        unique_chicken = "Тестовая курица 888"
        
        # Добавляем несколько продуктов
        await product_service.add_product(
            CreateProductIn(
                title=unique_apple,
                carbs_100g=14.0,
                proteins_100g=0.3,
                fats_100g=0.2, 
                kcal_100g=52
            )
        )
        
        await product_service.add_product(
            CreateProductIn(
                title=unique_chicken,
                carbs_100g=0.0,
                proteins_100g=31.0,
                fats_100g=3.6,
                kcal_100g=165
            )
        )
        
        # Получаем список продуктов
        products = await product_service.list_products()
        
        # Ищем наши продукты
        our_products = [p for p in products if p.title in [unique_apple, unique_chicken]]
        
        # Проверяем что добавились именно наши продукты
        assert len(our_products) == 2
        product_titles = [p.title for p in our_products]
        assert unique_apple in product_titles
        assert unique_chicken in product_titles