# Centros Docentes de Andalucía · buscador por cercanía en coche

Aplicación para **ordenar tus preferencias de destino** como docente: pones tu
punto de partida, filtras por etapa, **enseñanza concreta**, titularidad,
provincia y municipio, y la app ordena los centros por **distancia y tiempo
reales** según el **modo de transporte** (coche 🚗, transporte público 🚌,
bici 🚲 o andando 🚶) con Google Maps. Puedes marcar centros con ★, reordenarlos
y **descargar tu lista de preferencias en CSV** (en ese orden y con todos los
campos del directorio de origen).

📚 Documentación detallada en [`docs/`](docs/README.md):
[API](docs/api.md) · [Backend](docs/backend.md) · [Frontend](docs/frontend.md).

## Cómo se usa (paso a paso)

1. **Punto de partida** (arriba a la izquierda): escribe tu dirección y pulsa
   *Buscar*, usa *Usar mi ubicación actual*, o haz clic en el mapa. Es necesario
   para ordenar por cercanía.
2. **Filtra** por provincia, municipio, titularidad y etapa/enseñanza concreta.
   La lista se reduce y se reordena por cercanía.
3. **Elige el modo de transporte** (🚗 🚌 🚲 🚶) en la cabecera de resultados
   para ver tiempo y distancia reales, y el criterio de orden.
4. **Marca** los centros que te interesen pulsando la **estrella ☆** de cada
   tarjeta (pasa a ★). Aparecen en **⭐ Mis preferencias**, en la barra izquierda.
5. **Ordénalos** en ese panel con las flechas **▲ ▼**. El número (1, 2, 3…) es
   el orden que tendrá el CSV.
6. Pulsa **⬇ Descargar CSV**: se descarga `mis-centros-preferidos.csv` en ese
   orden y con **todos los campos** del directorio. (Tus preferencias se guardan
   en el navegador, no se pierden al recargar.)

### Pestaña «Buscar / Listado»

- **Buscar centro** por nombre o código y ver sus datos.
- **Resolver listado**: pega o sube un fichero (`.txt`, `.csv`, `.xlsx`, `.pdf`)
  con códigos de centro y obtén sus **nombres** (copiar, descargar `.txt` o CSV
  completo). Detecta los códigos automáticamente, **incluido el PDF del concurso
  de traslados** (apartado «Peticiones a centros»). Filtra por prefijo de
  provincia para no confundirlos con DNI, teléfonos, etc.

Datos: [Directorio de Centros Docentes de Andalucía](https://www.juntadeandalucia.es/datosabiertos/portal/dataset/directorio-de-centros-docentes-de-andalucia)
(Junta de Andalucía, CC BY 4.0), curso **2024/2025** — 7.106 centros.

## Arquitectura

```
Navegador ──► Frontend (React + Vite, servido por nginx)
                   │  /api  (proxy)
                   ▼
              Backend (FastAPI)
                   ├─ centros.json  (datos en memoria, orden por línea recta)
                   └─ Google Maps   (geocoding + distancia/tiempo en coche)
```

- **Línea recta** (haversine): instantánea, gratis, para el primer orden.
- **Coche** (Google Distance Matrix): para todos los centros filtrados (lotes de
  25 en paralelo), con caché en el backend para no repetir llamadas. La clave de
  Google vive **solo en el backend**.
- Mapa: Leaflet + OpenStreetMap (tiles gratis), Google solo donde aporta.

## Estructura

```
backend/      FastAPI + Dockerfile (multi-stage: base → test → prod)
  app/
    main.py            app y rutas (OpenAPI en /api/docs)
    routers/           meta, centros, google_routes (geocode + distancias)
    google.py          cliente Google Maps + caché
    geo.py             haversine
    data/              centros.json + meta.json (generados)
  tests/               suite pytest (Google mockeado)
frontend/     React + Vite + Dockerfile (nginx)
scripts/preprocess.py     CSV oficial -> JSON limpio
datos/                    CSV originales descargados
docs/                     documentación (api, backend, frontend)
docker-compose.yml        base = PRODUCCIÓN
docker-compose.override.yml  DESARROLLO (auto en `docker compose up`)
docker-compose.test.yml   tests con pytest
.env                      GOOGLE_MAPS_API_KEY (NO se sube a git)
```

## Puesta en marcha (desarrollo)

Requisitos: Docker, Node 18+, Python 3.11+.

1. Asegúrate de que `.env` tiene tu clave:
   ```
   GOOGLE_MAPS_API_KEY=...
   ```
2. (Solo si cambian los CSV) regenera los datos:
   ```bash
   python scripts/preprocess.py
   ```
3. Backend (Docker, con recarga). `docker compose up` aplica
   automáticamente `docker-compose.override.yml` (desarrollo), que monta el
   código, activa `--reload` y publica el puerto 8000. El frontend NO arranca
   aquí (está tras el profile `prod`):
   ```bash
   docker compose up -d        # solo backend, en modo dev (:8000)
   ```
   O sin Docker:
   ```bash
   cd backend && python -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   .venv\Scripts\uvicorn app.main:app --reload
   ```
4. Frontend:
   ```bash
   cd frontend && npm install && npm run dev
   ```
   Abre http://localhost:5173 (Vite redirige `/api` a `http://localhost:8000`).

### Convención de ficheros Compose

| Fichero | Rol | Cuándo se aplica |
|---|---|---|
| `docker-compose.yml` | **Base = producción** | Siempre (explícito en prod). |
| `docker-compose.override.yml` | **Desarrollo** (recarga, código montado, :8000) | Automático en `docker compose up`. |
| `docker-compose.test.yml` | Tests (pytest) | Explícito con `-f`. |

## Tests (pytest en contenedor)

Antes de construir la imagen de producción, pasa la batería de tests dentro de
un contenedor (Google va mockeado, no necesita clave ni red):

```bash
docker compose -f docker-compose.test.yml run --rm tests
```

## Construir y poner en marcha en producción

En producción se usa el **base explícito** (`-f docker-compose.yml`), que ignora
el override de desarrollo, con el **profile `prod`** para incluir el frontend:

```bash
# 1) (recomendado) ejecutar los tests
docker compose -f docker-compose.test.yml run --rm tests

# 2) construir y levantar backend + frontend en segundo plano
docker compose -f docker-compose.yml --profile prod up -d --build

# ver el estado y los logs
docker compose -f docker-compose.yml --profile prod ps
docker compose -f docker-compose.yml --profile prod logs -f

# parar
docker compose -f docker-compose.yml --profile prod down
```

La app queda en `http://localhost:8080` (o el `FRONTEND_PORT` que definas).
La API y su documentación Swagger están en `/api` y `/api/docs`.

## Despliegue en producción (VPS Hostinger)

1. Sube el proyecto al VPS (git o scp). El `.env` con la clave debe existir allí.
2. Ajusta en `.env`:
   ```
   FRONTEND_PORT=8080
   CORS_ORIGINS=https://centros.tudominio.com
   ```
3. Levanta (base explícito + profile `prod`, para no aplicar el override de dev):
   ```bash
   docker compose -f docker-compose.yml --profile prod up -d --build
   ```
   El frontend queda en `http://IP_DEL_VPS:8080` y hace de proxy a la API.

### Integración con tu proxy inverso

Si ya usas un reverse proxy (Nginx Proxy Manager, Traefik, Caddy) para tus
otros contenedores, apúntalo al servicio `frontend` (puerto 80) y gestiona ahí
el dominio y el HTTPS. Como solo se publica el frontend y la API va por la red
interna de Docker, no choca con tus otros contenedores.

## La API

El backend es una **API REST** documentada con OpenAPI. Con la app en marcha:

- Swagger UI: `/api/docs`  ·  ReDoc: `/api/redoc`  ·  Esquema: `/api/openapi.json`

| Método | Ruta              | Descripción                                          |
|--------|-------------------|------------------------------------------------------|
| GET    | `/api/health`     | Estado y nº de centros.                              |
| GET    | `/api/meta`       | Catálogo de filtros (provincias, municipios, etapas→enseñanzas).|
| GET    | `/api/centros`    | Filtra (etapa, enseñanza concreta, titularidad…) y ordena por cercanía.|
| POST   | `/api/geocode`    | Dirección → lat/lng.                                 |
| POST   | `/api/distancias` | Distancia/tiempo a una lista de centros, por modo de transporte.|
| POST   | `/api/export`     | CSV de los centros marcados, en orden y con todos los campos de origen.|
| POST   | `/api/lookup`     | Resuelve una lista de códigos a nombres y datos básicos.|

Referencia completa de parámetros y ejemplos: [`docs/api.md`](docs/api.md).

## Seguridad de la clave de Google ⚠️

- La clave **no** se incluye en el frontend; solo la usa el backend.
- En Google Cloud Console, **restringe la clave**: limita las APIs a *Geocoding*
  y *Distance Matrix*, y restringe por IP a la de tu VPS.
- La clave compartida por chat debería **rotarse**: créala de nuevo y sustitúyela
  en `.env`.

## Datos: actualizar a un nuevo curso

Descarga el CSV del nuevo curso a `datos/`, ajusta la ruta en
`scripts/preprocess.py` y vuelve a ejecutarlo. Las columnas de enseñanzas
cambian de nombre entre cursos; el script avisa si alguna del catálogo no
aparece en el CSV.
