from functools import lru_cache
from pydantic_settings import BaseSettings


@lru_cache()
def get_settings():
    return Settings()

class Settings(BaseSettings):
    POSTGRES_PASSWORD : str
    POSTGRES_USER : str
    POSTGRES_DB : str
    POSTGRES_PORT : str
    POSTGRES_NAME : str