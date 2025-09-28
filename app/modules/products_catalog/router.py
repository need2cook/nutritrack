from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProductsOut, AddProductOut, CreateProductIn
from .service import ProductService

from app.core.sessionmaker_fastapi import db_sessions

from loguru import logger


router = APIRouter()


@router.post("/", response_model=AddProductOut)
async def add_product(
    payload: CreateProductIn,
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    svc = ProductService(session)    
    await svc.add_product(payload)

    return AddProductOut(success=True)

@router.get("/", response_model=list[ProductsOut])
async def get_products(
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    svc = ProductService(session)
    products = await svc.list_products()
    return products