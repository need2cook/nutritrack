from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_sessions

from app.config import settings
from app.tg_bot import bot
from .schemas.private import AddProductOut, CreateProductIn
from .schemas.public import ProductsOut
from app.db import ProductDAO

from loguru import logger


router = APIRouter()


@router.post("/product", response_model=AddProductOut)
async def add_product(
    payload: CreateProductIn,
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    product = await ProductDAO.find_one_or_none(session, title=payload.title)
    if product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Продукт уже добавлен.'
        )

    await ProductDAO.add(session, **(payload.model_dump()))

    return AddProductOut(success=True)


@router.get("/products", response_model=list[ProductsOut])
async def get_products(
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    return await ProductDAO.find_all(session)
