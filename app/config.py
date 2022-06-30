from pydantic import BaseSettings


class Bot(BaseSettings):
    token: str


class Settings(BaseSettings):
    bot: Bot

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "_"


def load_config(env_file: str = ".env") -> Settings:
    return Settings(_env_file=env_file)
