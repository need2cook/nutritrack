from loguru import logger
import asyncio
import os

from app.core.config import settings



class TelegramLogHandler:
    def __init__(self, bot, info_channel):
        self.bot = bot
        self.info_channel = info_channel
        

    async def send_log(self, message: str, level: str):
        try:
            await self.bot.send_message(chat_id=self.info_channel, text=message)
        except Exception as e:
            print(f"Не удалось отправить лог в Telegram: {e}")

    def __call__(self, message):
        record = message.record
        level = record["level"].name
        time_str = record["time"].strftime("%d.%m.%Y %H:%M:%S")
        log_text = f"[{time_str}] | {record['message']}"
        asyncio.create_task(self.send_log(log_text, level))


def init_logger(bot):
    logger.add(
        os.path.join(settings.LOGS_DIR, 'info.log'),
        format="<green>{time:DD.MM.YYYY HH:mm:ss}</green> | <level>{level}</level> | {message}",
        level="INFO",
        rotation="100 KB",
        compression="zip"
    )

    logger.add(
        os.path.join(settings.LOGS_DIR, 'errors.log'),
        format="<green>{time:DD.MM.YYYY HH:mm:ss}</green> | <level>{level}</level> | {message}",
        level="ERROR",
        rotation="100 KB",
        compression="zip"
    )

    logger.add(
        TelegramLogHandler(
            bot,
            settings.LOGS_CHANNEL_ID,
        ),
        level="WARNING",
    )
