from typing import Any

import httpx

from app.schemas.municipio import FreguesiaResponse, MunicipioResponse

GEO_API_BASE_URL = "https://json.geoapi.pt"
GEO_API_TIMEOUT_SECONDS = 10.0


class MunicipioNotFoundError(Exception):
    """Raised when GEO API PT cannot find the requested municipality."""


class GeoApiUnavailableError(Exception):
    """Raised when GEO API PT cannot provide a usable response."""


def _area_km2(data: dict[str, Any]) -> float | None:
    """Convert the documented total area in hectares to square kilometres."""
    geojson = data.get("geojson")
    if isinstance(geojson, dict):
        properties = geojson.get("properties")
        if isinstance(properties, dict):
            area_ha = properties.get("Area_T_ha")
            if area_ha is not None and not isinstance(area_ha, bool):
                try:
                    return float(area_ha) / 100
                except (TypeError, ValueError):
                    return None

    return None


def _freguesias(data: dict[str, Any]) -> list[str]:
    raw_freguesias = data.get("freguesias")
    if isinstance(raw_freguesias, list):
        return [item for item in raw_freguesias if isinstance(item, str)]

    geojsons = data.get("geojsons")
    if not isinstance(geojsons, dict):
        return []

    features = geojsons.get("freguesias")
    if not isinstance(features, list):
        return []

    freguesias: list[str] = []
    for feature in features:
        if not isinstance(feature, dict):
            continue

        properties = feature.get("properties")
        if not isinstance(properties, dict):
            continue

        nome = properties.get("freguesia")
        if isinstance(nome, str) and nome:
            freguesias.append(nome)

    return freguesias


def _normalize_municipio(data: dict[str, Any]) -> MunicipioResponse:
    nome = data.get("nome")
    if not isinstance(nome, str) or not nome:
        raise ValueError("GEO API PT response has no municipality name")

    dtmn = data.get("dtmn")
    codigo_ine = data.get("codigoine")

    return MunicipioResponse(
        nome=nome,
        dtmn=str(dtmn) if dtmn is not None else None,
        codigoine=str(codigo_ine) if codigo_ine is not None else None,
        freguesias=_freguesias(data),
    )


def _normalize_freguesia(data: dict[str, Any]) -> FreguesiaResponse:
    nome = data.get("nome")
    if not isinstance(nome, str) or not nome:
        raise ValueError("GEO API PT response has no freguesia name")

    codigo_ine = data.get("codigoine")

    return FreguesiaResponse(
        nome=nome,
        codigo_ine=str(codigo_ine) if codigo_ine is not None else None,
    )


async def get_municipio(nome: str) -> MunicipioResponse:
    """Fetch and normalize one municipality from GEO API PT."""
    try:
        async with httpx.AsyncClient(
            base_url=GEO_API_BASE_URL,
            timeout=GEO_API_TIMEOUT_SECONDS,
        ) as client:
            response = await client.get(f"/municipio/{nome}")
    except httpx.RequestError as exc:
        raise GeoApiUnavailableError from exc

    if response.status_code == 404:
        raise MunicipioNotFoundError

    try:
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise TypeError("Unexpected GEO API PT response")
        return _normalize_municipio(payload)
    except (httpx.HTTPStatusError, TypeError, ValueError) as exc:
        raise GeoApiUnavailableError from exc


async def get_freguesias_por_municipio(nome: str) -> list[FreguesiaResponse]:
    """Fetch and normalize a list of freguesias of one municipio from GEO API PT."""
    try:
        async with httpx.AsyncClient(
            base_url=GEO_API_BASE_URL,
            timeout=GEO_API_TIMEOUT_SECONDS,
        ) as client:
            response = await client.get(f"/municipio/{nome}/freguesias")
    except httpx.RequestError as exc:
        raise GeoApiUnavailableError from exc

    if response.status_code == 404:
        raise MunicipioNotFoundError

    try:
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise TypeError("Unexpected GEO API PT response")
        return [
            _normalize_freguesia(item)
            for item in payload
            if isinstance(item, dict)
        ]
    except (httpx.HTTPStatusError, TypeError, ValueError) as exc:
        raise GeoApiUnavailableError from exc
