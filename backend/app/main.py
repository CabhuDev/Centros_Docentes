from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .data_store import store
from .routers import centros, export, google_routes, lookup, meta

DESCRIPTION = """
API REST del buscador de **Centros Docentes de Andalucía**.

Permite filtrar centros (provincia, municipio, titularidad, etapa y enseñanza
concreta), ordenarlos por cercanía en línea recta, geocodificar una dirección y
calcular distancia y tiempo reales por modo de transporte (Google Maps).

Datos: Directorio oficial de la Junta de Andalucía (CC BY 4.0), curso 2024/2025.
"""

tags_metadata = [
    {"name": "meta", "description": "Catálogo para construir los filtros."},
    {"name": "centros", "description": "Listado, filtrado y orden por cercanía."},
    {"name": "rutas", "description": "Geocodificación y distancias/tiempos (Google Maps)."},
    {"name": "exportar", "description": "Descargar centros seleccionados a CSV."},
    {"name": "lookup", "description": "Resolver una lista de códigos a nombres."},
    {"name": "salud", "description": "Estado del servicio."},
]

app = FastAPI(
    title="Centros Docentes de Andalucía · API",
    description=DESCRIPTION,
    version="1.1.0",
    # Documentacion accesible tambien tras el proxy nginx (prefijo /api).
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meta.router, prefix="/api", tags=["meta"])
app.include_router(centros.router, prefix="/api", tags=["centros"])
app.include_router(google_routes.router, prefix="/api", tags=["rutas"])
app.include_router(export.router, prefix="/api", tags=["exportar"])
app.include_router(lookup.router, prefix="/api", tags=["lookup"])


@app.get("/api/health", tags=["salud"])
def health() -> dict:
    return {
        "status": "ok",
        "total_centros": len(store.centros),
        "curso": store.meta.get("curso"),
        "google_key_configurada": bool(settings.google_maps_api_key),
    }
