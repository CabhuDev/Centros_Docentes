from __future__ import annotations

import unicodedata

from fastapi import APIRouter, Query

from ..config import settings
from ..data_store import store
from ..geo import haversine_km

router = APIRouter()


def _norm(s: str) -> str:
    """Minusculas y sin acentos, para comparar de forma robusta."""
    s = (s or "").strip().lower()
    return "".join(
        ch for ch in unicodedata.normalize("NFD", s)
        if unicodedata.category(ch) != "Mn"
    )


@router.get("/centros")
def list_centros(
    provincia: str | None = None,
    municipio: list[str] | None = Query(default=None),
    titularidad: str | None = None,
    concertado: bool | None = None,
    etapas: list[str] | None = Query(default=None),
    etapas_match: str = Query(default="any", pattern="^(any|all)$"),
    ensenanzas: list[str] | None = Query(default=None),
    ensenanzas_match: str = Query(default="any", pattern="^(any|all)$"),
    regimen_general: bool | None = None,
    regimen_adultos: bool | None = None,
    regimen_especial: bool | None = None,
    q: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    limit: int | None = None,
) -> dict:
    """Devuelve centros filtrados. Si se pasa lat/lng, anade distancia en linea
    recta (km) y ordena por cercania; si no, ordena por nombre."""
    municipios = {_norm(m) for m in municipio} if municipio else None
    etapas_set = set(etapas) if etapas else None
    ensenanzas_set = set(ensenanzas) if ensenanzas else None
    qn = _norm(q) if q else None

    out = []
    for c in store.centros:
        if provincia and _norm(c["provincia"]) != _norm(provincia):
            continue
        if municipios and _norm(c["municipio"]) not in municipios:
            continue
        if titularidad and _norm(c["titularidad"]) != _norm(titularidad):
            continue
        if concertado is not None and c["concertado"] != concertado:
            continue
        if regimen_general is not None and c["regimen_general"] != regimen_general:
            continue
        if regimen_adultos is not None and c["regimen_adultos"] != regimen_adultos:
            continue
        if regimen_especial is not None and c["regimen_especial"] != regimen_especial:
            continue
        if etapas_set:
            ce = set(c["etapas"])
            if etapas_match == "all":
                if not etapas_set.issubset(ce):
                    continue
            else:  # any
                if not (etapas_set & ce):
                    continue
        if ensenanzas_set:
            cen = set(c["ensenanzas"])
            if ensenanzas_match == "all":
                if not ensenanzas_set.issubset(cen):
                    continue
            else:  # any
                if not (ensenanzas_set & cen):
                    continue
        if qn:
            blob = f"{c['nombre']} {c['municipio']} {c['localidad']} {c['codigo']}".lower()
            if qn not in blob:
                continue

        item = dict(c)
        if lat is not None and lng is not None and c["lat"] is not None:
            item["distancia_recta_km"] = round(
                haversine_km(lat, lng, c["lat"], c["lng"]), 2
            )
        out.append(item)

    if lat is not None and lng is not None:
        out.sort(key=lambda x: x.get("distancia_recta_km", float("inf")))
    else:
        out.sort(key=lambda x: _norm(x["nombre"]))

    total = len(out)
    cap = limit or settings.max_results
    return {"total": total, "devueltos": min(total, cap), "items": out[:cap]}
