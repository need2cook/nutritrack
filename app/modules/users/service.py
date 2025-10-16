from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from loguru import logger

from .dao import UserDAO
from .models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_profile(
        self,
        user_id: int
    ):
        return await UserDAO.find_one_or_none_by_id(self.session, data_id=user_id)
    

    async def edit_weight(
        self,
        user_id: int,
        new_weight: float,
    ):
        try:
            await UserDAO.update(
                self.session,
                {'id': user_id},
                current_weight=new_weight,
            )
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Неизвестная ошибка в edit_weight: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Что-то пошло не так, попробуйте позже.."
            )
