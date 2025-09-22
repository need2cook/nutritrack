from fastapi import APIRouter, Depends
from app.utils import verify_and_set_initdata, ensure_user_via_upsert
from app.db import User

router = APIRouter()


@router.post("/handshake")
async def auth_handshake(user: User = Depends(ensure_user_via_upsert)):
    return {"ok": True, "user_id": user.id}
