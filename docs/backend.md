# Backend

API REST en **FastAPI** (Python 3.12). Sirve los datos de centros ya
procesados y orquesta las llamadas a Google Maps. La clave de Google vive solo
aquí; el navegador nunca la ve.

## Estructura

```
backend/
├─ app/
│  ├─ main.py            App FastAPI, CORS, montaje de routers, /api/health, OpenAPI en /api/docs
│  ├─ config.py          Settings (pydantic-settings): GOOGLE_MAPS_API_KEY, CORS, max_results
│  ├─ data_store.py      Carga centros.json + meta.json en memoria al arrancar
│  ├─ geo.py             haversine_km (distancia en línea recta)
│  ├─ google.py          Cliente Google (geocode + distance_matrix) con caché en memoria
│  ├─ models.py          Modelos Pydantic de petición/respuesta
│  ├─ routers/
│  │  ├─ meta.py            GET /api/meta
│  │  ├─ centros.py         GET /api/centros (filtros + orden por cercanía)
│  │  ├─ google_routes.py   POST /api/geocode, POST /api/distancias
│  │  ├─ export.py          POST /api/export (CSV en orden, todos los campos)
│  │  └─ lookup.py          POST /api/lookup (códigos → nombres)
│  └─ data/
│     ├─ centros.json     7.106 centros normalizados (generado)
│     ├─ meta.json        Catálogo de filtros (generado)
│     └─ centros_raw.json Filas originales completas, 89 columnas (generado)
├─ tests/                Suite pytest (Google mockeado)
├─ requirements.txt      Dependencias de producción
├─ requirements-dev.txt  + pytest
├─ pytest.ini
└─ Dockerfile            Multi-stage: base → test → prod
```

## Flujo de una búsqueda

1. El frontend pide `GET /api/centros` con filtros y, si hay origen, `lat`/`lng`.
2. El backend filtra en memoria y ordena por **haversine** (instantáneo, gratis).
3. El frontend pide `POST /api/distancias` para todos los centros devueltos.
4. El backend llama a **Google Distance Matrix** por lotes de 25 destinos, **en
   paralelo** (semáforo de 5 lotes), y cachea cada resultado
   `(origen, centro, modo)` para no repetir llamadas.

## Datos

Los JSON los genera `scripts/preprocess.py` a partir del CSV oficial
(`datos/centros_24-25.csv`). El script:

- Detecta la codificación (UTF-8 con respaldo latin-1).
- Parsea coordenadas con coma decimal.
- Agrupa las ~69 columnas `S/N` en **etapas** (nivel grueso) y **enseñanzas**
  (modalidad concreta: ordinario / adultos / distancia / regladas…).
- Avisa si alguna columna del catálogo no aparece en el CSV (los nombres cambian
  entre cursos).
- Conserva además la **fila original completa** (`centros_raw.json`) para poder
  exportar a CSV todos los campos de origen sin perder ninguna columna.

Para actualizar a un curso nuevo: coloca el CSV en `datos/`, ajusta la ruta en
`preprocess.py` y reejecútalo.

## Configuración (variables de entorno)

| Variable               | Por defecto                              | Descripción                          |
|------------------------|------------------------------------------|--------------------------------------|
| `GOOGLE_MAPS_API_KEY`  | —                                        | Clave de Geocoding + Distance Matrix.|
| `CORS_ORIGINS`         | `http://localhost:5173,http://localhost:4173` | Orígenes permitidos (coma).     |
| `MAX_RESULTS`          | `800`                                    | Tope de centros por consulta.        |

Se leen de `.env` (raíz del proyecto) o del entorno del contenedor.

## Ejecutar con Docker (desarrollo)

`docker compose up` aplica automáticamente `docker-compose.override.yml`
(desarrollo): monta `app/`, activa `--reload` y publica el puerto 8000. El
frontend no arranca aquí (va por `npm run dev`).

```bash
docker compose up -d        # backend en modo dev (:8000)
```

Convención de ficheros Compose:

| Fichero | Rol | Cuándo |
|---|---|---|
| `docker-compose.yml` | Base = **producción** | Explícito (`-f`, profile `prod`). |
| `docker-compose.override.yml` | **Desarrollo** | Automático en `docker compose up`. |
| `docker-compose.test.yml` | Tests | Explícito (`-f`). |

## Ejecutar en local (sin Docker)

```bash
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements-dev.txt
.venv\Scripts\uvicorn app.main:app --reload
```

## Tests

```bash
# en local
cd backend && .venv\Scripts\python -m pytest

# en contenedor
docker compose -f docker-compose.test.yml run --rm tests
```

Los tests mockean Google, así que no necesitan clave ni red.
