"""Exportar la lista de centros seleccionados a CSV, en el orden indicado y
con TODOS los campos del directorio de origen."""
from __future__ import annotations

import csv
import io

from fastapi import APIRouter, HTTPException, Response

from ..data_store import store
from ..models import ExportRequest

router = APIRouter()

MODE_LABEL = {
    "driving": "coche",
    "transit": "transporte publico",
    "bicycling": "bici",
    "walking": "andando",
}


@router.post("/export", tags=["exportar"])
def export_csv(req: ExportRequest) -> Response:
    """Devuelve un CSV (UTF-8 con BOM, separador ';') con los centros indicados
    en el mismo orden recibido. Incluye el orden de preferencia, los datos de
    viaje (si se aportan) y todas las columnas originales del directorio."""
    columns = store.raw_columns

    # ¿Algun centro trae datos de viaje calculados? Si es asi, anadimos columnas.
    hay_viaje = any(
        it.duration_text or it.distance_text or it.distancia_recta_km is not None
        for it in req.items
    )
    cols_viaje = (
        ["modo_transporte", "tiempo_viaje", "distancia_ruta", "distancia_recta_km"]
        if hay_viaje else []
    )
    cabecera = ["orden_preferencia"] + cols_viaje + columns

    sio = io.StringIO()
    writer = csv.writer(sio, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(cabecera)

    escritos = 0
    for i, it in enumerate(req.items, start=1):
        raw = store.raw_by_codigo.get(it.codigo)
        if raw is None:
            continue
        fila = [i]
        if cols_viaje:
            fila += [
                MODE_LABEL.get(req.mode, req.mode),
                it.duration_text or "",
                it.distance_text or "",
                it.distancia_recta_km if it.distancia_recta_km is not None else "",
            ]
        fila += [raw.get(c, "") for c in columns]
        writer.writerow(fila)
        escritos += 1

    if escritos == 0:
        raise HTTPException(status_code=400, detail="Ningun centro valido para exportar.")

    # BOM para que Excel reconozca UTF-8 y muestre bien los acentos.
    contenido = "﻿" + sio.getvalue()
    return Response(
        content=contenido.encode("utf-8"),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="mis-centros-preferidos.csv"'
        },
    )
