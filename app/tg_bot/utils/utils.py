from app.modules.users.dao import UserDAO
from app.modules.diaries.service import DiaryService
from app.modules.diaries.models import Day

from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

import math


async def get_today_day(user_tg_id: int, session: AsyncSession):
    user = await UserDAO.find_one_or_none(session, telegram_id=user_tg_id)

    if not user:
        logger.error(f"Пользователь не найден в today в тг боте")
        return

    svc = DiaryService(session)

    data = await svc.get_today(
        user_id=user.id,
        diary_id=user.diary.id,
    )

    return data


def get_products_data(day: Day):
    products_data = {
        'total_kcal': 0,
        'total_prots': 0,
        'total_carbs': 0,
        'total_fats': 0,
        "products": []
    }
    for product in day.product_entries:
        products_data['products'].append(
            {
                "title": product.product.title,
                "kcal": math.ceil(product.product.kcal_100g / 100 * product.grams),
                "prots": math.ceil(product.product.proteins_100g / 100 * product.grams),
                "carbs": math.ceil(product.product.carbs_100g / 100 * product.grams),
                "fats": math.ceil(product.product.fats_100g / 100 * product.grams),
                "grams": math.ceil(product.grams),
            }
        )

        products_data['total_kcal'] += math.ceil(
            product.product.kcal_100g / 100 * product.grams)
        products_data['total_prots'] += math.ceil(
            product.product.proteins_100g / 100 * product.grams)
        products_data['total_carbs'] += math.ceil(
            product.product.carbs_100g / 100 * product.grams)
        products_data['total_fats'] += math.ceil(
            product.product.fats_100g / 100 * product.grams)

    return products_data


def get_exercise_data(day: Day):
    exercise_data = {
        'total_kcal': 0,
        'exercises': [],
    }
    for exer in day.exersice_entries:
        exercise_data['exercises'].append(
            {
                "title": exer.exersice.title,
                "kcal": math.ceil(exer.exersice.kcal_30m / 30 * exer.minutes),
                "minutes": exer.minutes
            }
        )
        exercise_data['total_kcal'] += math.ceil(
            exer.exersice.kcal_30m / 30 * exer.minutes)

    return exercise_data


def format_today_output(day: Day) -> str:
    products_data = get_products_data(day)
    exercise_data = get_exercise_data(day)

    text = f'<b>Статистика за {day.date}</b>\n\n'

    text += f"<b>Питание</b> • <code>{products_data['total_kcal']} ккал</code>\n"
    text += "<blockquote>"

    for product in products_data['products']:
        text += (
            f"• {product['title']}: <code>{product['grams']}г</code> • "
            f"<code>{product['prots']}/{product['fats']}/{product['carbs']}</code> "
            f"• <code>{product['kcal']}ккал</code>\n"
        )

    text += '\n'
    text += f"<b>Белки:</b> <code>{products_data['total_prots']}г</code>\n"
    text += f"<b>Жиры:</b> <code>{products_data['total_fats']}г</code>\n"
    text += f"<b>Углеводы:</b> <code>{products_data['total_carbs']}г</code>"

    text += "</blockquote>\n\n"

    text += f"<b>Упражнения</b> • <code>{exercise_data['total_kcal']} ккал</code>\n"
    text += "<blockquote>"

    for exer in exercise_data['exercises']:
        text += (
            f"• {exer['title']}: <code>{exer['minutes']}м</code> • "
            f"<code>{exer['kcal']}ккал</code>\n"
        )

    text += "</blockquote>\n\n"

    text += f"<b>Воды выпито:</b> <code>{day.water_drinked_ml}мл</code>"

    return text
