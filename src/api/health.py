from fastapi import APIRouter

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@health_router.get("/status", summary="Проверка жизни сервиса")
async def get_status():
    return {"status": "ok"}
