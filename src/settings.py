import yaml

from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import SecretStr

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
BASE_DIR = Path(__file__).resolve().parent

__all__ = ("BASE_DIR", "DATETIME_FORMAT", "settings")


class _AppSettings(BaseSettings):
    name: str = "VULSA"
    host: str = '0.0.0.0'
    port: int = 8000
    secret_key: SecretStr
    debug: bool = True

    def get_app_url(self):
        return f"http://{self.host}:{self.port}"


class _DatabaseSettings(BaseSettings):
    user: str
    password: SecretStr
    host: str = 'localhost'
    port: int = 5432
    name: str = 'postgres'

    def get_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class _CacheSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379

    def get_url(self, db_num: int = 0):
        return f"redis://{self.host}:{self.port}/{db_num}"


class _Settings(BaseSettings):
    app: _AppSettings
    database: _DatabaseSettings
    cache: _CacheSettings

    @classmethod
    def load(cls) -> "_Settings":
        path = Path(BASE_DIR.parent, "config", "config.yaml")

        if path.exists():
            with open(path) as file:
                return cls(**yaml.safe_load(file))

        raise FileNotFoundError(f"Could not find config.yaml in {path}")


settings = _Settings.load()