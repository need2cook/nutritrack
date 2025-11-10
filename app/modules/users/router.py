from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth import AuthService
from app.core.sessionmaker_fastapi import db_sessions

from .service import UserService
from .models import User
from .schemas import ProfileOut, Success, EditWeightIn, EditGoalIn


router = APIRouter()


@router.get('/me', response_model=ProfileOut)
async def get_user_profile(
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = UserService(session)
    data = await svc.get_profile(
        user_id=user.id
    )

    return data


@router.put('/me/weight', response_model=Success)
async def edit_weight(
    payload: EditWeightIn,
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = UserService(session)

    await svc.edit_weight(
        user_id=user.id,
        new_weight=payload.new_weight
    )

    return Success(success=True)



@router.put('/me/goal', response_model=Success)
async def edit_goal(
    payload: EditGoalIn,
    user: "User" = Depends(AuthService.get_current_user_readonly),
    session: AsyncSession = Depends(db_sessions.get_db),
):
    svc = UserService(session)

    await svc.edit_goal(
        user_id=user.id,
        new_goal=payload.new_goal,
    )

    return Success(success=True)