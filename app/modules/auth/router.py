from fastapi import APIRouter, Depends
from .service import AuthService

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.users.models import User


router = APIRouter()


@router.post("/handshake")
async def auth_handshake(user: "User" = Depends(AuthService.ensure_user_via_upsert)):
    return {"ok": True, "user_id": user.id}
