from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.submission import Submission
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.widget_repository import WidgetRepository
from app.schemas.submission import SubmissionCreate


class SubmissionService:
    def __init__(self, db: Session):
        self.submissions = SubmissionRepository(db)
        self.widgets = WidgetRepository(db)

    def create(
        self,
        widget_id: int,
        data: SubmissionCreate,
        ip_address: str | None,
    ) -> Submission:
        widget = self.widgets.get_public_by_id(widget_id)

        if widget is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Widget not found",
            )

        allowed_fields = {
            field["name"]
            for field in widget.fields
        }

        submitted_fields = set(data.data.keys())

        if not submitted_fields.issubset(allowed_fields):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Submission contains unknown fields",
            )

        for field in widget.fields:
            if field.get("required") and not data.data.get(field["name"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field['name']}",
                )

        submission = Submission(
            widget_id=widget.id,
            data=data.data,
            ip_address=ip_address,
        )

        return self.submissions.create(submission)