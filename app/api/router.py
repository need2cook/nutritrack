from fastapi import APIRouter, Depends

from app.modules.users.router import router as user_router
from app.modules.diaries.router import router as diary_router
from app.modules.exersices_catalog.router import router as exercise_router
from app.modules.products_catalog.router import router as products_router
from app.modules.auth.router import router as auth_router

from app.modules.auth import AuthService


api_v1 = APIRouter(prefix='/api/v1', tags=['NutriTrack API V1'], dependencies=[Depends(AuthService.verify_and_set_initdata)])

# include-ы
api_v1.include_router(user_router, prefix='/users', tags=['users'])
api_v1.include_router(diary_router, prefix='/diaries', tags=['diaries'])
api_v1.include_router(exercise_router, prefix='/exercises_catalog', tags=['exercises_catalog'])
api_v1.include_router(products_router, prefix='/products_catalog', tags=['products_catalog'])
api_v1.include_router(auth_router, prefix='/auth', tags=["auth"])

