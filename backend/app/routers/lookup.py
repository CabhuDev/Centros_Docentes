"""Resolver una lista de codigos de centro a sus nombres y datos basicos."""
from __future__ import annotations

from fastapi import APIRouter

from ..data_store import store
from ..models import LookupItem, LookupRequest, LookupResponse

router = APIRouter()


def _buscar(codigo: str) -> dict | None:
    cod = (codigo or "").strip()
    c = store.by_codigo.get(cod)
    if c is None and cod.isdigit():
        # algunos listados pierden el cero inicial: probamos rellenando a 8.
        c = store.by_codigo.get(cod.zfill(8))
    return c


@router.post("/lookup", response_model=LookupResponse, tags=["lookup"])
def lookup(req: LookupRequest) -> LookupResponse:
    """Devuelve, en el mismo orden, el centro de cada codigo (o encontrado=false)."""
    items: list[LookupItem] = []
    encontrados = 0
    for codigo in req.codigos:
        c = _buscar(codigo)
        if c is not None:
            encontrados += 1
            items.append(LookupItem(
                codigo=c["codigo"], encontrado=True, nombre=c["nombre"],
                denominacion=c["denominacion"], municipio=c["municipio"],
                provincia=c["provincia"], titularidad=c["titularidad"],
            ))
        else:
            items.append(LookupItem(codigo=(codigo or "").strip(), encontrado=False))
    return LookupResponse(items=items, total=len(items), encontrados=encontrados)
