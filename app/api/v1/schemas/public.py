from pydantic import BaseModel, field_validator


class ProductsOut(BaseModel):
    id: int
    title: str
    carbs_100g: float
    proteins_100g: float
    fats_100g: float
    kcal_100g: int
