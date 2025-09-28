import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int]

    # DB
    POSTGRES_DRIVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DBNAME: str

    @computed_field(return_type=str)
    @property
    def DB_URL(self) -> str:
        return (
            f"{self.POSTGRES_DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DBNAME}"
        )

    BASE_SITE: str
    FRONT_SITE: str

    LOGS_CHANNEL_ID: int
    ###########################
    # ПУТИ
    ###########################
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ENV_DIR: str = os.path.join(BASE_DIR, ".env")
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs/")

    model_config = SettingsConfigDict(
        env_file=ENV_DIR
    )

    def get_webhook_url(self) -> str:
        """Возвращает URL вебхука."""
        return f"{self.BASE_SITE}/webhook"


# Инициализация настроек и планировщика задач
settings = Settings()
database_url = settings.DB_URL