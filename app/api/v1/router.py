from fastapi import APIRouter, Depends
from .public import router as public_router
from .private import router as private_router
from .auth import router as auth_router

from app.utils import verify_and_set_initdata

api_v1 = APIRouter(prefix='/api/v1', tags=['NutriTrack API V1'])
api_v1.include_router(public_router, prefix='/public', tags=['Public API'])
api_v1.include_router(private_router, prefix='/private',
                      tags=['Private API'], dependencies=[Depends(verify_and_set_initdata)])
api_v1.include_router(auth_router, prefix='/auth',
                      tags=["Auth API"], dependencies=[Depends(verify_and_set_initdata)])
