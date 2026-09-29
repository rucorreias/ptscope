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
    async def mock_get(*_args, **_kwargs) -> httpx.Response:
        return make_geoapi_response(
            200,
            {
                "nome": "Porto",
                "dtmn": "1312",
                "codigoine": "1312",
                "distrito": "Porto",
                "areaha": "41.29",
                "geojson": {"properties": {"Area_T_ha": 4145.6}},
                "geojsons": {
                    "freguesias": [
                        {"properties": {"freguesia": "Bonfim"}},
                        {"properties": {"freguesia": "Campanhã"}},
                        {"properties": {"freguesia": "Paranhos"}},
                        {"properties": {"freguesia": "Ramalde"}},
                        {
                            "properties": {
                                "freguesia": "União das freguesias de Aldoar, "
                                "Foz do Douro e Nevogilde"
                            }
                        },
                        {
                            "properties": {
                                "freguesia": "União das freguesias de Cedofeita, "
                                "Santo Ildefonso, Sé, Miragaia, "
                                "São Nicolau e Vitória"
                            }
                        },
                        {
                            "properties": {
                                "freguesia": "União das freguesias de Lordelo "
                                "do Ouro e Massarelos"
                            }
                        },
                    ]
                },
                "populacao": 231800,
            },
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    response = client.get("/api/v1/municipios/porto")

    assert response.status_code == 200
    assert response.json() == {
        "nome": "Porto",
        "dtmn": "1312",
        "codigoine": "1312",
        "freguesias": [
            "Bonfim",
            "Campanhã",
            "Paranhos",
            "Ramalde",
            "União das freguesias de Aldoar, Foz do Douro e Nevogilde",
            "União das freguesias de Cedofeita, Santo Ildefonso, Sé, "
            "Miragaia, São Nicolau e Vitória",
            "União das freguesias de Lordelo do Ouro e Massarelos",
        ],
    }


def test_municipio_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_get(*_args, **_kwargs) -> httpx.Response:
        return make_geoapi_response(
            404,
            {"erro": "Município não encontrado!"},
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    response = client.get("/api/v1/municipios/desconhecido")

    assert response.status_code == 404
    assert response.json() == {"detail": "Município não encontrado"}


def test_geoapi_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_get(*_args, **_kwargs) -> httpx.Response:
        request = httpx.Request("GET", "https://json.geoapi.pt/municipio/porto")
        raise httpx.ConnectError("GEO API PT unavailable", request=request)

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    response = client.get("/api/v1/municipios/porto")

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Não foi possível obter dados da GEO API PT"
    }


def test_municipio_area_is_converted_from_hectares() -> None:
    area_km2 = geoapi._area_km2(  # pylint: disable=protected-access
        {"geojson": {"properties": {"Area_T_ha": 4145.6}}}
    )

    assert area_km2 == 41.456


def test_municipio_area_does_not_use_ambiguous_areaha() -> None:
    area_km2 = geoapi._area_km2({"areaha": "41.29"})  # pylint: disable=protected-access

    assert area_km2 is None


def test_municipio_area_is_none_when_total_hectares_are_invalid() -> None:
    area_km2 = geoapi._area_km2(  # pylint: disable=protected-access
        {"geojson": {"properties": {"Area_T_ha": "invalid"}}}
    )

    assert area_km2 is None
