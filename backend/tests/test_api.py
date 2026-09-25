import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import geoapi

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"project": "PTScope", "status": "running"}


def test_health() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def make_geoapi_response(status_code: int, json: dict[str, object]) -> httpx.Response:
    request = httpx.Request("GET", "https://json.geoapi.pt/municipio/porto")
    return httpx.Response(status_code, json=json, request=request)


def test_municipio_is_normalized(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_get(*args, **kwargs) -> httpx.Response:
        return make_geoapi_response(
            200,
            {
                "nome": "Porto",
                "codigoine": "1312",
                "distrito": "Porto",
                "areaha": "41.29",
                "geojson": {"properties": {"Area_T_ha": 4145.6}},
                "populacao": 231800,
            },
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    response = client.get("/api/v1/municipios/porto")

    assert response.status_code == 200
    assert response.json() == {
        "nome": "Porto",
        "codigo_ine": "1312",
        "distrito": "Porto",
        "area_km2": 41.456,
    }


def test_municipio_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_get(*args, **kwargs) -> httpx.Response:
        return make_geoapi_response(
            404,
            {"erro": "Município não encontrado!"},
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    response = client.get("/api/v1/municipios/desconhecido")

    assert response.status_code == 404
    assert response.json() == {"detail": "Município não encontrado"}


def test_geoapi_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_get(*args, **kwargs) -> httpx.Response:
        request = httpx.Request("GET", "https://json.geoapi.pt/municipio/porto")
        raise httpx.ConnectError("GEO API PT unavailable", request=request)

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    response = client.get("/api/v1/municipios/porto")

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Não foi possível obter dados da GEO API PT"
    }


def test_municipio_area_is_converted_from_hectares() -> None:
    municipio = geoapi._normalize_municipio(
        {
            "nome": "Porto",
            "geojson": {"properties": {"Area_T_ha": 4145.6}},
        }
    )

    assert municipio.area_km2 == 41.456
