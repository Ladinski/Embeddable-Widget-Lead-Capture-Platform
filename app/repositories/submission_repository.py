from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.submission import Submission
from app.models.widget import Widget


class SubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, submission: Submission) -> Submission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def get_by_owner(
        self,
        owner_id: int,
        widget_id: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Submission]:
        statement = (
            select(Submission)
            .join(Widget, Submission.widget_id == Widget.id)
            .where(Widget.owner_id == owner_id)
            .order_by(Submission.created_at.desc())
        )

        if widget_id is not None:
            statement = statement.where(
                Submission.widget_id == widget_id
            )

        statement = statement.limit(limit).offset(offset)

        return list(self.db.scalars(statement).all())

    def count_by_owner(self, owner_id: int) -> int:
        statement = (
            select(func.count(Submission.id))
            .join(Widget, Submission.widget_id == Widget.id)
            .where(Widget.owner_id == owner_id)
        )

        return self.db.scalar(statement) or 0

    def count_per_widget(
        self,
        owner_id: int,
    ) -> list[tuple[int, int]]:
        statement = (
            select(
                Submission.widget_id,
                func.count(Submission.id),
            )
            .join(Widget, Submission.widget_id == Widget.id)
            .where(Widget.owner_id == owner_id)
            .group_by(Submission.widget_id)
            .order_by(Submission.widget_id)
        )

        return list(self.db.execute(statement).all())

    def count_by_country(
        self,
        owner_id: int,
    ) -> list[tuple[str | None, int]]:
        statement = (
            select(
                Submission.country,
                func.count(Submission.id),
            )
            .join(Widget, Submission.widget_id == Widget.id)
            .where(Widget.owner_id == owner_id)
            .group_by(Submission.country)
            .order_by(func.count(Submission.id).desc())
        )

        return list(self.db.execute(statement).all())