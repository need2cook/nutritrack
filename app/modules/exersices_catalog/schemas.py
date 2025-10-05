from pydantic import BaseModel, field_validator


class ExercisesOut(BaseModel):
    id: int
    title: str
    kcal_30m: int

