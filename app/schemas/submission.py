from datetime import datetime
from typing import Any

from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    data: dict[str, Any]


class SubmissionResponse(BaseModel):
    id: int
    widget_id: int
    data: dict[str, Any]
    country: str | None
    city: str | None
    created_at: datetime

    class Config:
        from_attributes = True