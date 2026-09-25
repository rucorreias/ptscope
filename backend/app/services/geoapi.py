from typing import Any

import httpx

from app.schemas.municipio import MunicipioResponse


GEO_API_BASE_URL = "https://json.geoapi.pt"
GEO_API_TIMEOUT_SECONDS = 10.0


class MunicipioNotFoundError(Exception):
    """Raised when GEO API PT cannot find the requested municipality."""


class GeoApiUnavailableError(Exception):
    """Raised when GEO API PT cannot provide a usable response."""


def _area_km2(data: dict[str, Any]) -> float | None:
    """Normalize the best available municipality area to square kilometres."""
    geojson = data.get("geojson")
    if isinstance(geojson, dict):
        properties = geojson.get("properties")
        if isinstance(properties, dict) and properties.get("Area_T_ha") is not None:
            return float(properties["Area_T_ha"]) / 100

    # The legacy municipality field is named `areaha`, but its values are km2.
    legacy_area = data.get("areaha")
    return float(legacy_area) if legacy_area is not None else None


def _normalize_municipio(data: dict[str, Any]) -> MunicipioResponse:
    nome = data.get("nome")
    if not isinstance(nome, str) or not nome:
        raise ValueError("GEO API PT response has no municipality name")

    codigo_ine = data.get("codigoine")
    distrito = data.get("distrito")

    return MunicipioResponse(
        nome=nome,
        codigo_ine=str(codigo_ine) if codigo_ine is not None else None,
        distrito=str(distrito) if distrito is not None else None,
        area_km2=_area_km2(data),
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
            raise ValueError("Unexpected GEO API PT response")
        return _normalize_municipio(payload)
    except (httpx.HTTPStatusError, TypeError, ValueError) as exc:
        raise GeoApiUnavailableError from exc
