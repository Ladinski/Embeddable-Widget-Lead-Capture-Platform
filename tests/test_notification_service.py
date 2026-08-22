from app.services.notification_service import NotificationService


def test_notification_service_runs():
    service = NotificationService()

    service.send_submission_notification(
        widget_id=1,
        submission_id=1,
    )