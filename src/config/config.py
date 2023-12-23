from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Конфиг приложения
    """

    TITLE: str = "Kriging interpolation"
    SUMMARY: str = "Приложение для работы с интерполяционными методами кригинга"
    VERSION: str = "0.1.0"
    
    MONGO_URI: str
    MONGO_DB_NAME: str = Field(alias="MONGO_INITDB_DATABASE")

    model_config = SettingsConfigDict(env_file='../env', env_file_encoding='utf-8')


settings = Settings()
