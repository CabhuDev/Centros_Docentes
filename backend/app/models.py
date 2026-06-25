"""Modelos Pydantic de peticion/respuesta."""
from __future__ import annotations

from pydantic import BaseModel, Field


class LatLng(BaseModel):
    lat: float
    lng: float


class GeocodeRequest(BaseModel):
    address: str = Field(min_length=2)


class GeocodeResponse(BaseModel):
    lat: float
    lng: float
    formatted_address: str


class DistanciasRequest(BaseModel):
    origin: LatLng
    codigos: list[str] = Field(min_length=1, max_length=600)
    mode: str = "driving"  # driving | walking | bicycling | transit


class DistanciaItem(BaseModel):
    codigo: str
    status: str
    distance_m: int | None = None
    distance_text: str | None = None
    duration_s: int | None = None
    duration_text: str | None = None


class DistanciasResponse(BaseModel):
    results: list[DistanciaItem]


class ExportItem(BaseModel):
    codigo: str
    distancia_recta_km: float | None = None
    distance_text: str | None = None
    duration_text: str | None = None


class ExportRequest(BaseModel):
    items: list[ExportItem] = Field(min_length=1, max_length=2000)
    mode: str = "driving"


class LookupRequest(BaseModel):
    codigos: list[str] = Field(min_length=1, max_length=3000)


class LookupItem(BaseModel):
    codigo: str
    encontrado: bool
    nombre: str | None = None
    denominacion: str | None = None
    municipio: str | None = None
    provincia: str | None = None
    titularidad: str | None = None


class LookupResponse(BaseModel):
    items: list[LookupItem]
    total: int
    encontrados: int
