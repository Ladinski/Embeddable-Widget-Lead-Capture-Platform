from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.widget import Widget


def seed():
    db = SessionLocal()

    try:
        user = db.scalar(
            select(User).where(User.email == "demo@example.com")
        )

        if user is None:
            user = User(
                email="demo@example.com",
                hashed_password=hash_password("demo1234"),
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        widget = db.scalar(
            select(Widget).where(
                Widget.owner_id == user.id,
                Widget.title == "Contact Us",
            )
        )

        if widget is None:
            widget = Widget(
                owner_id=user.id,
                type="contact",
                title="Contact Us",
                description="Send us a message",
                button_text="Send",
                fields=[
                    {
                        "name": "email",
                        "type": "email",
                        "required": True,
                    },
                    {
                        "name": "message",
                        "type": "text",
                        "required": True,
                    },
                ],
                is_active=True,
            )

            db.add(widget)
            db.commit()

        print("Seed complete")
        print("Email: demo@example.com")
        print("Password: demo1234")

    finally:
        db.close()


if __name__ == "__main__":
    seed()