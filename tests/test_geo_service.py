from app.services.geo_service import GeoService


def test_provider_a_success(monkeypatch):
    service = GeoService()

    monkeypatch.setattr(
        service,
        "_provider_a",
        lambda ip: {
            "country": "North Macedonia",
            "city": "Skopje",
            "provider": "ip-api",
        },
    )

    monkeypatch.setattr(
        service,
        "_provider_b",
        lambda ip: None,
    )

    result = service.lookup("8.8.8.8")

    assert result["country"] == "North Macedonia"
    assert result["city"] == "Skopje"
    assert result["provider"] == "ip-api"


def test_provider_b_used_when_a_fails(monkeypatch):
    service = GeoService()

    monkeypatch.setattr(
        service,
        "_provider_a",
        lambda ip: None,
    )

    monkeypatch.setattr(
        service,
        "_provider_b",
        lambda ip: {
            "country": "United States",
            "city": "Mountain View",
            "provider": "ipapi",
        },
    )

    result = service.lookup("8.8.8.8")

    assert result["country"] == "United States"
    assert result["city"] == "Mountain View"
    assert result["provider"] == "ipapi"


def test_submission_continues_when_all_providers_fail(monkeypatch):
    service = GeoService()

    monkeypatch.setattr(
        service,
        "_provider_a",
        lambda ip: None,
    )

    monkeypatch.setattr(
        service,
        "_provider_b",
        lambda ip: None,
    )

    result = service.lookup("8.8.8.8")

    assert result == {}


def test_private_ip_skips_geo_lookup():
    service = GeoService()

    result = service.lookup("172.18.0.1")

    assert result == {}