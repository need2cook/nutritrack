from app.modules.base import BaseDAO
from .models import Product


class ProductDAO(BaseDAO):
    model = Product