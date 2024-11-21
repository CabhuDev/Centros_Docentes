from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import api_routes
from fastapi.staticfiles import StaticFiles

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Centros Educativos API",
    description="Backend para manejar consultas de centros educativos.",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las origenes (configurar en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas del enrutador
app.include_router(api_routes.router, prefix="/api", tags=["Centros"])

# Ruta raíz
@app.get("/")
async def root():
    return {"mensaje": "Bienvenido a la API de Centros Educativos"}

# Monta la carpeta 'frontend' para servir los archivos estáticos
app.mount("/CentrosEducativos", StaticFiles(directory="frontend", html=True), name="frontend")