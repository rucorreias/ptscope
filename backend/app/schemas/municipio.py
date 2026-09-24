from pydantic import BaseModel


class MunicipioResponse(BaseModel):
    nome: str
    codigo_ine: str | None = None
    distrito: str | None = None
    area_km2: float | None = None
