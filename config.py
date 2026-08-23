from typing import final
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

@final
class Config(BaseSettings):  # pyright: ignore
    model_provider_base_url: str = "https://api.deepseek.com"
    model_provider_api_key: str = Field(default="")
    model_name: str = "deepseek-v4-flash"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_configs() -> Config:
    return Config()
