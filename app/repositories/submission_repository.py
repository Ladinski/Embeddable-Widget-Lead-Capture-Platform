from sqlalchemy.orm import Session

from app.models.submission import Submission


class SubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, submission: Submission) -> Submission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission