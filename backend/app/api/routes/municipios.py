from fastapi import APIRouter, HTTPException, status

from app.schemas.municipio import MunicipioResponse
from app.services import geoapi

router = APIRouter(prefix="/municipios", tags=["municipios"])


@router.get("/{nome}", response_model=MunicipioResponse)
async def get_municipio(nome: str) -> MunicipioResponse:
    """Return normalized municipality data from GEO API PT."""
    try:
        return await geoapi.get_municipio(nome)
    except geoapi.MunicipioNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Município não encontrado",
        ) from None
    except geoapi.GeoApiUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Não foi possível obter dados da GEO API PT",
        ) from None
