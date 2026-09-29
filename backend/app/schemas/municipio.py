from pydantic import BaseModel


class MunicipioResponse(BaseModel):
    nome: str
    dtmn: str | None = None
    codigoine: str | None = None
    freguesias: list[str] = []


class FreguesiaResponse(BaseModel):
    nome: str
    codigo_ine: str | None = None
