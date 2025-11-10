from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from app.modules.users.dao import UserDAO
from app.modules.diaries.service import DiaryService

from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from app.tg_bot.utils.utils import get_today_day, format_today_output


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text="Добро пожаловать в <b>NutriTrack</b>.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Статистика за сегодня', callback_data='today')]
        ])
    )


@router.callback_query(F.data == 'today')
async def today(callback: CallbackQuery, session: AsyncSession):
    try:
        day = await get_today_day(user_tg_id=callback.from_user.id, session=session)

        await callback.message.edit_text(
            text=format_today_output(day),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Назад", callback_data='back')]
                ]
            )
        )
    except Exception as e:
        logger.error(f"Ошибка в today: {e}")



@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Добро пожаловать в <b>NutriTrack</b>.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Статистика за сегодня', callback_data='today')]
        ])
    )
