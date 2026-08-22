from sqlalchemy.orm import Session

from app.repositories.submission_repository import SubmissionRepository


class DashboardService:
    def __init__(self, db: Session):
        self.repository = SubmissionRepository(db)

    def get_submissions(
        self,
        owner_id: int,
        widget_id: int | None,
        limit: int,
        offset: int,
    ):
        return self.repository.get_by_owner(
            owner_id=owner_id,
            widget_id=widget_id,
            limit=limit,
            offset=offset,
        )

    def get_stats(self, owner_id: int) -> dict:
        total = self.repository.count_by_owner(owner_id)

        widget_counts = self.repository.count_per_widget(
            owner_id
        )

        country_counts = self.repository.count_by_country(
            owner_id
        )

        return {
            "total_submissions": total,
            "submissions_per_widget": [
                {
                    "widget_id": widget_id,
                    "count": count,
                }
                for widget_id, count in widget_counts
            ],
            "country_breakdown": [
                {
                    "country": country or "Unknown",
                    "count": count,
                }
                for country, count in country_counts
            ],
        }