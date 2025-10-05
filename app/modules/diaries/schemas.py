from pydantic import BaseModel, field_validator
from datetime import date


class ProductOut(BaseModel):
    id: int
    title: str

    carbs_100g: float
    proteins_100g: float
    fats_100g: float
    kcal_100g: int

class ExerciseOut(BaseModel):
    id: int
    title: str

    kcal_30m: int


class ProductEntryOut(BaseModel):
    id: int
    product: ProductOut
    grams: int

class ExersiceEntryOut(BaseModel):
    id: int
    exersice: ExerciseOut
    minutes: int

class DayOut(BaseModel):
    id: int
    date: date

    model_config = {"from_attributes": True}

    product_entries: list[ProductEntryOut] | None
    exersice_entries: list[ExersiceEntryOut] | None


class AddProductIn(BaseModel):
    target_date: date
    product_id: int
    grams: int

    @field_validator("grams")
    @classmethod
    def grams_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Количество граммов должно быть > 0")
        return v


class CreateProductIn(BaseModel):
    title: str
    carbs_100g: float
    proteins_100g: float
    fats_100g: float
    kcal_100g: int


class AddProductOut(BaseModel):
    success: bool


class AddExerciseOut(BaseModel):
    success: bool


class DeleteProductIn(BaseModel):
    target_date: date
    entry_id: int


class DeleteProductOut(BaseModel):
    success: bool


class DeleteExerciseOut(BaseModel):
    success: bool



class AddExerciseIn(BaseModel):
    target_date: date
    exercise_id: int
    minutes: int

    @field_validator("minutes")
    @classmethod
    def minutes_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Количество минут должно быть > 0")
        return v