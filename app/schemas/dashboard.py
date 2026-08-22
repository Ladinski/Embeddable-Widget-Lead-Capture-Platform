from datetime import datetime
from typing import Any

from pydantic import BaseModel


class DashboardSubmissionResponse(BaseModel):
    id: int
    widget_id: int
    data: dict[str, Any]
    country: str | None
    city: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class WidgetSubmissionCount(BaseModel):
    widget_id: int
    count: int


class CountrySubmissionCount(BaseModel):
    country: str
    count: int


class DashboardStatsResponse(BaseModel):
    total_submissions: int
    submissions_per_widget: list[WidgetSubmissionCount]
    country_breakdown: list[CountrySubmissionCount]