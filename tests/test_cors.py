def test_cors_preflight(client):
    response = client.options(
        "/public/widgets/1/submissions",
        headers={
            "Origin": "http://localhost:5500",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5500"
    )

    assert "POST" in response.headers[
        "access-control-allow-methods"
    ]