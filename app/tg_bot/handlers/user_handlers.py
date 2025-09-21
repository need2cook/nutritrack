from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text="Добро пожаловать в <b>NutriTrack</b>."
    )