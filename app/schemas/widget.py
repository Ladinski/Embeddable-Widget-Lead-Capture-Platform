from datetime import datetime

from pydantic import BaseModel, Field


class WidgetField(BaseModel):
    name: str
    type: str
    required: bool = False


class WidgetCreate(BaseModel):
    type: str
    title: str
    description: str | None = None
    button_text: str = "Submit"
    fields: list[WidgetField] = Field(default_factory=list)


class WidgetUpdate(BaseModel):
    type: str | None = None
    title: str | None = None
    description: str | None = None
    button_text: str | None = None
    fields: list[WidgetField] | None = None
    is_active: bool | None = None


class WidgetResponse(BaseModel):
    id: int
    owner_id: int
    type: str
    title: str
    description: str | None
    button_text: str
    fields: list[WidgetField]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PublicWidgetConfig(BaseModel):
    id: int
    type: str
    title: str
    description: str | None
    button_text: str
    fields: list[WidgetField]
    
class EmbedResponse(BaseModel):
    snippet: str