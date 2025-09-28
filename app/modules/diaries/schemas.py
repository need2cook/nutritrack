from pydantic import BaseModel, field_validator
from datetime import date


class ProductOut(BaseModel):
    id: int
    title: str

    carbs_100g: float
    proteins_100g: float
    fats_100g: float
    kcal_100g: int


class ProductEntryOut(BaseModel):
    id: int
    product: ProductOut
    grams: int


class DayOut(BaseModel):
    id: int
    date: date

    model_config = {"from_attributes": True}

    product_entries: list[ProductEntryOut] | None


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
