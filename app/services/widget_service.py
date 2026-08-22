from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.widget import Widget
from app.repositories.widget_repository import WidgetRepository
from app.schemas.widget import WidgetCreate, WidgetUpdate


class WidgetService:
    def __init__(self, db: Session):
        self.repository = WidgetRepository(db)

    def create(
        self,
        owner_id: int,
        data: WidgetCreate,
    ) -> Widget:
        widget = Widget(
            owner_id=owner_id,
            type=data.type,
            title=data.title,
            description=data.description,
            button_text=data.button_text,
            fields=[field.model_dump() for field in data.fields],
        )

        return self.repository.create(widget)

    def get_all(self, owner_id: int) -> list[Widget]:
        return self.repository.get_all_by_owner(owner_id)

    def get_one(
        self,
        widget_id: int,
        owner_id: int,
    ) -> Widget:
        widget = self.repository.get_by_id_and_owner(
            widget_id,
            owner_id,
        )

        if widget is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Widget not found",
            )

        return widget

    def update(
        self,
        widget_id: int,
        owner_id: int,
        data: WidgetUpdate,
    ) -> Widget:
        widget = self.get_one(widget_id, owner_id)

        updates = data.model_dump(exclude_unset=True)

        if "fields" in updates and updates["fields"] is not None:
            updates["fields"] = [
                field.model_dump()
                for field in data.fields
            ]

        for field, value in updates.items():
            setattr(widget, field, value)

        return self.repository.save(widget)

    def delete(
        self,
        widget_id: int,
        owner_id: int,
    ) -> None:
        widget = self.get_one(widget_id, owner_id)
        self.repository.delete(widget)

    def get_public_config(self, widget_id: int) -> Widget:
        widget = self.repository.get_public_by_id(widget_id)

        if widget is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Widget not found",
            )

        return widget

    def get_embed_snippet(
        self,
        widget_id: int,
        owner_id: int,
    ) -> str:
        widget = self.get_one(widget_id, owner_id)

        return (
            f'<script src="{settings.base_url}/static/widget.js'
            f'?id={widget.id}"></script>'
        )