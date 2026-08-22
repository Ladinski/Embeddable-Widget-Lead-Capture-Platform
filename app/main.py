from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers.submissions import router as submissions_router
from app.core.config import settings
from app.routers.auth import router as auth_router
from app.routers.public_widgets import router as public_widgets_router
from app.routers.widgets import router as widgets_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(auth_router)
app.include_router(widgets_router)
app.include_router(public_widgets_router)
app.include_router(submissions_router)

@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}