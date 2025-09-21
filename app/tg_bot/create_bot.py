from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.tg_bot.logger import init_logger
from app.config import settings
from app.tg_bot.middlewares import TrackAllUsersMiddleware, DbSessionMiddleware
from app.db.database import async_session_maker

from loguru import logger

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

init_logger(bot)

dp.update.outer_middleware(DbSessionMiddleware(async_session_maker))
dp.callback_query.outer_middleware(TrackAllUsersMiddleware())
dp.message.outer_middleware(TrackAllUsersMiddleware())


async def start_bot():
    try:
        logger.warning(f"🟢 <b>@{(await bot.me()).username}</b> запущен..")
    except:
        pass


async def stop_bot():
    try:
        logger.warning(f"🔴 <b>@{(await bot.me()).username}</b> остановлен.")
    except:
        pass