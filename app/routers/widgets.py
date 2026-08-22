from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.widget import (
    WidgetCreate,
    WidgetResponse,
    WidgetUpdate,
)
from app.services.widget_service import WidgetService


router = APIRouter(
    prefix="/widgets",
    tags=["Widgets"],
)


@router.post(
    "",
    response_model=WidgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_widget(
    data: WidgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WidgetService(db)
    return service.create(current_user.id, data)


@router.get(
    "",
    response_model=list[WidgetResponse],
)
def get_widgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WidgetService(db)
    return service.get_all(current_user.id)


@router.get(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def get_widget(
    widget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WidgetService(db)
    return service.get_one(widget_id, current_user.id)


@router.put(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def update_widget(
    widget_id: int,
    data: WidgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WidgetService(db)

    return service.update(
        widget_id,
        current_user.id,
        data,
    )


@router.delete(
    "/{widget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_widget(
    widget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WidgetService(db)
    service.delete(widget_id, current_user.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)