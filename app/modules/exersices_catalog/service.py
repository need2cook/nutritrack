from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .dao import ExersiceDAO
from .models import Exersice
from .schemas import CreateExerciseIn
from fastapi import HTTPException, status


class ExerciseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_product(self, payload: CreateExerciseIn) -> None:
        try:
            await ExersiceDAO.add(self.session, **payload.model_dump())
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Упражнение уже добавлено.") from e
        except Exception:
            await self.session.rollback()
            raise

    async def list_exercises(self) -> list[Exersice]:
        return await ExersiceDAO.find_all(self.session)