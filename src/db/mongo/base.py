from config.config import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

mongo_client: AsyncIOMotorClient | None = None


def get_db() -> AsyncIOMotorDatabase:
    """Получить обьект бд mongo"""
    return mongo_client[settings.MONGO_DB_NAME]


def connect() -> None:
    """Соединение с mongodb"""
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI, uuidRepresentation="standard")


def disconnect() -> None:
    """Отклчение соеденения с mongodb"""
    global mongo_client
    mongo_client.close()
