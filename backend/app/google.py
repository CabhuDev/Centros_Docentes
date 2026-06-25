"""Cliente de las APIs de Google Maps (Geocoding + Distance Matrix).

La clave vive solo en el backend. Se cachean las distancias en memoria para
no repetir llamadas (y gastar cuota) con el mismo origen y centro.
"""
from __future__ import annotations

import asyncio

import httpx

from .config import settings

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
DISTANCE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

# Maximo de destinos por peticion a Distance Matrix con un unico origen.
DM_BATCH = 25

# Lotes simultaneos hacia Google (evita saturar la cuota por segundo).
DM_CONCURRENCY = 5

# Cache de distancias: clave (origin_redondeado, codigo, mode) -> dict
_distance_cache: dict[tuple, dict] = {}


class GoogleError(RuntimeError):
    pass


def _require_key() -> str:
    if not settings.google_maps_api_key:
        raise GoogleError("GOOGLE_MAPS_API_KEY no configurada en el backend.")
    return settings.google_maps_api_key


async def geocode(address: str) -> dict:
    """Devuelve {lat, lng, formatted_address} para una direccion."""
    key = _require_key()
    params = {
        "address": address,
        "key": key,
        "region": "es",
        "components": "country:ES",
        "language": "es",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(GEOCODE_URL, params=params)
        r.raise_for_status()
        data = r.json()

    status = data.get("status")
    if status == "ZERO_RESULTS" or not data.get("results"):
        raise GoogleError("No se encontro ninguna direccion para esa busqueda.")
    if status != "OK":
        raise GoogleError(f"Geocoding fallo: {status} {data.get('error_message', '')}")

    top = data["results"][0]
    loc = top["geometry"]["location"]
    return {
        "lat": loc["lat"],
        "lng": loc["lng"],
        "formatted_address": top.get("formatted_address", address),
    }


def _cache_key(origin: tuple[float, float], codigo: str, mode: str) -> tuple:
    # Redondeamos el origen a ~11 m para que cache sea efectiva.
    return (round(origin[0], 4), round(origin[1], 4), codigo, mode)


async def distance_matrix(
    origin: tuple[float, float],
    destinos: list[dict],
    mode: str = "driving",
) -> list[dict]:
    """destinos: lista de {codigo, lat, lng}. Devuelve una lista de resultados
    por codigo con distancia y duracion (o status de error)."""
    key = _require_key()
    results: dict[str, dict] = {}
    pendientes: list[dict] = []

    # 1) resolver desde cache lo que se pueda
    for d in destinos:
        ck = _cache_key(origin, d["codigo"], mode)
        cached = _distance_cache.get(ck)
        if cached is not None:
            results[d["codigo"]] = cached
        else:
            pendientes.append(d)

    # 2) llamar a Google por lotes (<=25 destinos) para lo no cacheado, EN
    #    PARALELO (con un semaforo). Un lote que falle NO tumba el resto: esos
    #    codigos quedan como ERROR (sin cachear, para reintentarse despues).
    lotes = [pendientes[i:i + DM_BATCH] for i in range(0, len(pendientes), DM_BATCH)]
    sem = asyncio.Semaphore(DM_CONCURRENCY)

    async with httpx.AsyncClient(timeout=20) as client:
        async def procesar(lote: list[dict]) -> None:
            async with sem:
                try:
                    elements = await _matrix_batch(client, origin, lote, mode, key)
                except (GoogleError, httpx.HTTPError):
                    for d in lote:
                        results[d["codigo"]] = {"codigo": d["codigo"], "status": "ERROR"}
                    return
            for d, el in zip(lote, elements):
                if el.get("status") == "OK":
                    res = {
                        "codigo": d["codigo"],
                        "status": "OK",
                        "distance_m": el["distance"]["value"],
                        "distance_text": el["distance"]["text"],
                        "duration_s": el["duration"]["value"],
                        "duration_text": el["duration"]["text"],
                    }
                    _distance_cache[_cache_key(origin, d["codigo"], mode)] = res
                else:
                    res = {"codigo": d["codigo"], "status": el.get("status", "ERROR")}
                results[d["codigo"]] = res

        await asyncio.gather(*(procesar(lote) for lote in lotes))

    # 3) devolver en el orden de entrada
    return [results[d["codigo"]] for d in destinos]


async def _matrix_batch(
    client: httpx.AsyncClient,
    origin: tuple[float, float],
    lote: list[dict],
    mode: str,
    key: str,
) -> list[dict]:
    """Una llamada a Distance Matrix para <=25 destinos. Reintenta una vez ante
    OVER_QUERY_LIMIT. Devuelve la lista de 'elements'."""
    params = {
        "origins": f"{origin[0]},{origin[1]}",
        "destinations": "|".join(f"{d['lat']},{d['lng']}" for d in lote),
        "mode": mode,
        "units": "metric",
        "language": "es",
        "key": key,
    }
    for intento in range(2):
        r = await client.get(DISTANCE_URL, params=params)
        r.raise_for_status()
        data = r.json()
        status = data.get("status")
        if status == "OK":
            return data["rows"][0]["elements"]
        if status == "OVER_QUERY_LIMIT" and intento == 0:
            await asyncio.sleep(0.4)
            continue
        raise GoogleError(
            f"Distance Matrix fallo: {status} {data.get('error_message', '')}"
        )
    raise GoogleError("Distance Matrix: OVER_QUERY_LIMIT")
