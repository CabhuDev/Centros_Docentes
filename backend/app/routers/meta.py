from fastapi import APIRouter

from ..data_store import store

router = APIRouter()


@router.get("/meta")
def get_meta() -> dict:
    """Catalogo para construir los filtros del frontend."""
    return store.meta
