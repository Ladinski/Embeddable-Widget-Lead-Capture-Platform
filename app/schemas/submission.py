from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SubmissionCreate(BaseModel):
    data: dict[str, Any]
    form_check: str | None = Field(default=None, max_length=200)


class SubmissionResponse(BaseModel):
    id: int
    widget_id: int
    data: dict[str, Any]
    country: str | None
    city: str | None
    created_at: datetime

    class Config:
        from_attributes = True