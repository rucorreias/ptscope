from fastapi import APIRouter


router = APIRouter(prefix="/municipios", tags=["municipios"])


@router.get("/{nome}")
def get_municipio(nome: str) -> dict[str, str]:
    """Return a placeholder response until the GEO API PT integration exists."""
    return {"municipio": nome, "status": "not_implemented"}
