from unittest.mock import MagicMock

from app.services.notification_service import NotificationService


def test_notification_failure_can_be_caught(monkeypatch):
    service = NotificationService()

    def fail(*args, **kwargs):
        raise RuntimeError("Notification provider down")

    monkeypatch.setattr(
        service,
        "send_submission_notification",
        fail,
    )

    try:
        service.send_submission_notification(
            widget_id=1,
            submission_id=1,
        )
    except RuntimeError:
        pass