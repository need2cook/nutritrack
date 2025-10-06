from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ExercisesOut, CreateExerciseIn, AddExerciseOut
from app.modules.auth import AuthService
from app.core.sessionmaker_fastapi import db_sessions
from .service import ExerciseService


router = APIRouter()


@router.post("/", response_model=AddExerciseOut)
async def add_product(
    payload: CreateExerciseIn,
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    svc = ExerciseService(session)    
    await svc.add_product(payload)

    return AddExerciseOut(success=True)


@router.get("/", response_model=list[ExercisesOut])
async def get_products(
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    svc = ExerciseService(session)
    exercises = await svc.list_exercises()
    return exercises