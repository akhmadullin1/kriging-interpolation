from celery import Celery

from config import settings

celery_client = Celery("tasks", broker=settings.REDIS_URI, include=["service.kriging.geospatial"])
