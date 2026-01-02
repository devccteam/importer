import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), '.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8')

    REDIS_PORT: str
    REDIS_HOST: str
    URL_API_PGRST: str
    CHUNK_TO_POST: int
    URL_API_DLL: str


settings = Settings()
