from api.router import api_router
from config.config import settings
from db.mongo.base import connect as mongo_connect
from db.mongo.base import disconnect as mongo_disconnect
from fastapi import FastAPI

app = FastAPI(
    title=settings.TITLE,
    summary=settings.SUMMARY,
    version=settings.VERSION,
)
app.include_router(api_router)
app.add_event_handler("startup", mongo_connect)
app.add_event_handler("shutdown", mongo_disconnect)
