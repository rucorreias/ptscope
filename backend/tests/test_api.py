from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"project": "PTScope", "status": "running"}


def test_health() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_municipio_placeholder() -> None:
    response = client.get("/api/v1/municipios/porto")

    assert response.status_code == 200
    assert response.json() == {
        "municipio": "porto",
        "status": "not_implemented",
    }
