from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.widget import PublicWidgetConfig
from app.services.widget_service import WidgetService


router = APIRouter(
    prefix="/public/widgets",
    tags=["Public Widgets"],
)


@router.get(
    "/{widget_id}/config",
    response_model=PublicWidgetConfig,
)
def get_widget_config(
    widget_id: int,
    response: Response,
    db: Session = Depends(get_db),
):
    service = WidgetService(db)

    widget = service.get_public_config(widget_id)

    response.headers["Cache-Control"] = "public, max-age=60"

    return widget