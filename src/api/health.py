from .router import api_router


@api_router.get("/status", summary="Проверка жизни сервиса", tags=["health"])
async def get_status():
    return {"status": "ok"}
