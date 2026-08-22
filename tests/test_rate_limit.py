from app.core.limiter import limiter


def test_rate_limit(client):
    limiter.enabled = True

    payload = {
        "data": {
            "email": "rate@example.com",
            "message": "hello",
        },
        "form_check": "",
    }

    status_codes = []

    for _ in range(6):
        response = client.post(
            "/public/widgets/1/submissions",
            json=payload,
        )
        status_codes.append(response.status_code)

    limiter.enabled = False

    assert 429 in status_codes