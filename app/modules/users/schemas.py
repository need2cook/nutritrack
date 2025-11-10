from pydantic import BaseModel, Field


class ProfileOut(BaseModel):
    username: str | None
    first_name: str
    current_weight: float | None
    goal: int | None

class Success(BaseModel):
    success: bool

class EditWeightIn(BaseModel):
    new_weight: float


class EditGoalIn(BaseModel):
    new_goal: int