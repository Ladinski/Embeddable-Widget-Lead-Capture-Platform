from fastapi import FastAPI

from app.core.config import settings
from app.routers.auth import router as auth_router
from app.routers.public_widgets import router as public_widgets_router
from app.routers.widgets import router as widgets_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(auth_router)
app.include_router(widgets_router)
app.include_router(public_widgets_router)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}