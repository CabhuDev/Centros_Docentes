from fastapi import APIRouter, HTTPException

from .. import google
from ..data_store import store
from ..models import (
    DistanciasRequest,
    DistanciasResponse,
    GeocodeRequest,
    GeocodeResponse,
)

router = APIRouter()


@router.post("/geocode", response_model=GeocodeResponse)
async def geocode(req: GeocodeRequest) -> GeocodeResponse:
    try:
        res = await google.geocode(req.address)
    except google.GoogleError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return GeocodeResponse(**res)


@router.post("/distancias", response_model=DistanciasResponse)
async def distancias(req: DistanciasRequest) -> DistanciasResponse:
    destinos = []
    for codigo in req.codigos:
        c = store.by_codigo.get(codigo)
        if c and c["lat"] is not None:
            destinos.append({"codigo": codigo, "lat": c["lat"], "lng": c["lng"]})

    if not destinos:
        raise HTTPException(status_code=400, detail="Ningun centro valido en la peticion.")

    try:
        results = await google.distance_matrix(
            (req.origin.lat, req.origin.lng), destinos, mode=req.mode
        )
    except google.GoogleError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return DistanciasResponse(results=results)
