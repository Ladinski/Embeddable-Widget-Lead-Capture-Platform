from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.services.submission_service import SubmissionService


router = APIRouter(
    prefix="/public/widgets",
    tags=["Public Submissions"],
)


@router.post(
    "/{widget_id}/submissions",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
def create_submission(
    request: Request,
    widget_id: int,
    data: SubmissionCreate,
    db: Session = Depends(get_db),
):
    service = SubmissionService(db)

    ip_address = request.client.host if request.client else None

    return service.create(
        widget_id,
        data,
        ip_address,
    )