from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.widget import Widget


class WidgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, widget: Widget) -> Widget:
        self.db.add(widget)
        self.db.commit()
        self.db.refresh(widget)
        return widget

    def get_all_by_owner(self, owner_id: int) -> list[Widget]:
        statement = select(Widget).where(
            Widget.owner_id == owner_id
        )

        return list(self.db.scalars(statement).all())

    def get_by_id_and_owner(
        self,
        widget_id: int,
        owner_id: int,
    ) -> Widget | None:
        statement = select(Widget).where(
            Widget.id == widget_id,
            Widget.owner_id == owner_id,
        )

        return self.db.scalar(statement)

    def delete(self, widget: Widget) -> None:
        self.db.delete(widget)
        self.db.commit()

    def save(self, widget: Widget) -> Widget:
        self.db.commit()
        self.db.refresh(widget)
        return widget

    def get_public_by_id(self, widget_id: int) -> Widget | None:
        statement = select(Widget).where(
            Widget.id == widget_id,
            Widget.is_active.is_(True),
        )

        return self.db.scalar(statement)