from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .dao import ExersiceDAO
from .models import Exersice
from fastapi import HTTPException, status


class ExerciseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_exercises(self) -> list[Exersice]:
        return await ExersiceDAO.find_all(self.session)