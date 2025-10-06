from pydantic import BaseModel, field_validator


class ExercisesOut(BaseModel):
    id: int
    title: str
    kcal_30m: int


class AddExerciseOut(BaseModel):
    success: bool

class CreateExerciseIn(BaseModel):
    title: str
    kcal_30m: int