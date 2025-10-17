from loguru import logger

from contextlib import asynccontextmanager

from app.tg_bot.create_bot import bot, dp, stop_bot, start_bot
from app.core.config import settings
from app.api.router import api_v1
from app.modules.pages.router import router as web_router
from app.tg_bot.handlers import routers

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request

from aiogram.types import Update

from alembic import command
from alembic.config import Config as AlembicConfig
import asyncio
import os

async def run_alembic_migration():
    try:
        BASE_DIR = settings.BASE_DIR
        alembic_cfg = AlembicConfig(os.path.join(BASE_DIR, "alembic.ini"))
        await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
    except Exception as e:
        raise

def run_migrations():
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(run_alembic_migration())
    except RuntimeError:
        asyncio.run(run_alembic_migration())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_bot()
    webhook_url = settings.get_webhook_url()

    run_migrations()

    dp.include_routers(*routers)

    await bot.set_webhook(
        url=f"{webhook_url}",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logger.info(f"Webhook URL: {webhook_url}")

    yield

    await bot.delete_webhook()
    await stop_bot()
    logger.info("Webhook удален")


app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='app/modules/pages/static'), 'static')


@app.post("/webhook")
async def main_webhook(request: Request):
    logger.info("Получили вебхук")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logger.info("Обработали вебхук")


app.include_router(api_v1)
app.include_router(web_router)
