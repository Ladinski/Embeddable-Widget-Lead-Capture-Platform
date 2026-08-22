import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.limiter import limiter
from app.core.database import Base, get_db
from app.main import app
from app.models import Submission, User, Widget


TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    user = User(
        email="test@example.com",
        hashed_password="test",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

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

    session.add(widget)
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    limiter.enabled = False

    with TestClient(app) as test_client:
        yield test_client

    limiter.enabled = True
    app.dependency_overrides.clear()