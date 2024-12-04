from functools import lru_cache
from inspari.config import load_dotenv
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    ENVIRONMENT: str
    CACHE_TYPE: str

    class Config:
        env_prefix = "APP_"


@lru_cache()
def app_settings() -> AppSettings:
    load_dotenv(dotenv_path="example.env")  # leave empty to load from .env
    return AppSettings()  # type: ignore
