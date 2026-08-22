from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.dashboard import (
    DashboardStatsResponse,
    DashboardSubmissionResponse,
)
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/submissions",
    response_model=list[DashboardSubmissionResponse],
)
def get_submissions(
    widget_id: int | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DashboardService(db)

    return service.get_submissions(
        owner_id=current_user.id,
        widget_id=widget_id,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
)
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DashboardService(db)

    return service.get_stats(current_user.id)