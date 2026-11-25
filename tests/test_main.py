import pytest
from fastapi.testclient import TestClient

from app import main

DEMO_SHA = "0123456789abcdef0123456789abcdef01234567"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "APP_COMMIT", DEMO_SHA)
    monkeypatch.setattr(main, "APP_VERSION", "v1.2.3")
    return TestClient(main.app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "v1.2.3", "commit": DEMO_SHA}


def test_home_renders_title_and_short_commit(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Plataforma Demo CI/CD" in response.text
    assert "<code>0123456</code>" in response.text
    assert DEMO_SHA not in response.text
