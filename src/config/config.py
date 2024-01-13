from enum import Enum, unique

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


@unique
class DataBaseType(Enum):
    """
    Типы баз даных
    """

    MONGO = 0


class ServiceTypes(BaseModel):
    """
    Типы баз данных, выбранных для серсисов
    """

    geo_kriging: DataBaseType = DataBaseType.MONGO
    coordinate: DataBaseType = DataBaseType.MONGO


class Settings(BaseSettings):
    """
    Конфиг приложения
    """

    TITLE: str = "Kriging interpolation"
    SUMMARY: str = "Приложение для работы с интерполяционными методами кригинга"
    VERSION: str = "0.2.1"

    MONGO_URI: str
    MONGO_DB_NAME: str = Field(alias="MONGO_INITDB_DATABASE")

    REDIS_URI: str

    service_types: ServiceTypes = ServiceTypes()

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
