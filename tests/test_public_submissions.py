from app.services.notification_service import NotificationService


def test_valid_submission(client):
    response = client.post(
        "/public/widgets/1/submissions",
        json={
            "data": {
                "email": "hello@example.com",
                "message": "Hello World",
            },
            "form_check": "",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["widget_id"] == 1
    assert body["data"]["email"] == "hello@example.com"


def test_missing_required_field(client):
    response = client.post(
        "/public/widgets/1/submissions",
        json={
            "data": {
                "email": "hello@example.com",
            },
            "form_check": "",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Missing required field: message"


def test_unknown_field_rejected(client):
    response = client.post(
        "/public/widgets/1/submissions",
        json={
            "data": {
                "email": "hello@example.com",
                "message": "Hello",
                "admin": "true",
            },
            "form_check": "",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Submission contains unknown fields"


def test_honeypot_rejects_spam(client):
    response = client.post(
        "/public/widgets/1/submissions",
        json={
            "data": {
                "email": "bot@example.com",
                "message": "Spam",
            },
            "form_check": "https://spam.example",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Spam submission rejected"


def test_oversized_field_rejected(client):
    response = client.post(
        "/public/widgets/1/submissions",
        json={
            "data": {
                "email": "hello@example.com",
                "message": "a" * 2001,
            },
            "form_check": "",
        },
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "Field value is too large"


def test_notification_failure_does_not_break_submission(
    client,
    monkeypatch,
):
    def fail_notification(*args, **kwargs):
        raise RuntimeError("Notification provider unavailable")

    monkeypatch.setattr(
        NotificationService,
        "send_submission_notification",
        fail_notification,
    )

    response = client.post(
        "/public/widgets/1/submissions",
        json={
            "data": {
                "email": "hello@example.com",
                "message": "Still store this",
            },
            "form_check": "",
        },
    )

    assert response.status_code == 201