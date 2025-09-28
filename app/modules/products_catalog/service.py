from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .dao import ProductDAO
from .schemas import CreateProductIn, ProductsOut
from .models import Product
from fastapi import HTTPException, status


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_product(self, payload: CreateProductIn) -> None:
        try:
            await ProductDAO.add(self.session, **payload.model_dump())
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Продукт уже добавлен.") from e
        except Exception:
            await self.session.rollback()
            raise

    async def list_products(self) -> list[Product]:
        return await ProductDAO.find_all(self.session)