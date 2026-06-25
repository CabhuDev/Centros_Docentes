# API · Centros Docentes de Andalucía

API REST construida con **FastAPI**. Documentación interactiva (OpenAPI) en
ejecución:

- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`
- Esquema OpenAPI: `/api/openapi.json`

Todas las rutas cuelgan de `/api`. En desarrollo el backend escucha en
`http://localhost:8000`; en producción se accede por el mismo dominio (nginx
hace de proxy de `/api` al backend).

Base URL (dev): `http://localhost:8000`

---

## GET /api/health

Estado del servicio.

**200 OK**
```json
{
  "status": "ok",
  "total_centros": 7106,
  "curso": "2024/2025",
  "google_key_configurada": true
}
```

---

## GET /api/meta

Catálogo para construir los filtros del frontend.

**200 OK** (resumido)
```json
{
  "curso": "2024/2025",
  "fuente": "Junta de Andalucía - Directorio de Centros Docentes (CC BY 4.0)",
  "total_centros": 7106,
  "provincias": ["Almería", "Cádiz", "..."],
  "municipios_por_provincia": { "Granada": ["Granada", "Motril", "..."] },
  "titularidades": ["Privado", "Público"],
  "denominaciones": ["Colegio de Educación Infantil y Primaria", "..."],
  "etapas": [
    {
      "key": "bachillerato",
      "label": "Bachillerato",
      "ensenanzas": [
        { "key": "bach_ord",  "label": "Bachillerato ordinario" },
        { "key": "bach_adul", "label": "Bachillerato para personas adultas" },
        { "key": "bach_dist", "label": "Bachillerato semipresencial / distancia" }
      ]
    }
  ]
}
```

---

## GET /api/centros

Filtra centros y, si se pasa `lat`/`lng`, añade la distancia en línea recta
(`distancia_recta_km`) y ordena por cercanía. Sin origen, ordena por nombre.

### Parámetros (query)

| Parámetro          | Tipo        | Descripción                                                        |
|--------------------|-------------|--------------------------------------------------------------------|
| `q`                | string      | Búsqueda libre (nombre, municipio, localidad, código).             |
| `provincia`        | string      | Provincia exacta (insensible a mayúsculas/acentos).                |
| `municipio`        | string (×N) | Uno o varios municipios.                                           |
| `titularidad`      | string      | `Público` o `Privado` (insensible a acentos).                      |
| `concertado`       | bool        | `true` para solo concertados.                                     |
| `etapas`           | string (×N) | Claves de etapa (p. ej. `eso`, `bachillerato`).                    |
| `etapas_match`     | `any`\|`all`| Imparte **alguna** (def.) o **todas** las etapas.                 |
| `ensenanzas`       | string (×N) | Claves de enseñanza concreta (p. ej. `bach_adul`, `fpgm_ord`).     |
| `ensenanzas_match` | `any`\|`all`| Imparte **alguna** (def.) o **todas** las enseñanzas.             |
| `regimen_general`  | bool        | Filtra por régimen general.                                       |
| `regimen_adultos`  | bool        | Filtra por régimen de adultos.                                    |
| `regimen_especial` | bool        | Filtra por régimen especial.                                      |
| `lat`, `lng`       | float       | Punto de partida; activa orden por cercanía.                      |
| `limit`            | int         | Máximo de resultados (def. 800).                                  |

### Ejemplo

```
GET /api/centros?provincia=Granada&titularidad=Público&ensenanzas=bach_ord&lat=37.1773&lng=-3.5986&limit=3
```

**200 OK**
```json
{
  "total": 145,
  "devueltos": 3,
  "items": [
    {
      "codigo": "18700430",
      "denominacion": "Instituto de Educación Secundaria",
      "nombre": "Padre Suárez",
      "titularidad": "Público",
      "concertado": false,
      "municipio": "Granada",
      "provincia": "Granada",
      "lat": 37.17, "lng": -3.60,
      "etapas": ["eso", "bachillerato"],
      "ensenanzas": ["eso", "bach_ord"],
      "distancia_recta_km": 0.68
    }
  ]
}
```

---

## POST /api/geocode

Convierte una dirección en coordenadas (Google Geocoding).

**Body**
```json
{ "address": "Gran Vía de Colón 21, Granada" }
```

**200 OK**
```json
{ "lat": 37.178, "lng": -3.599, "formatted_address": "C. Gran Vía de Colón, 21, 18001 Granada, España" }
```

Errores: `400` si no se encuentra la dirección o falta la clave de Google.

---

## POST /api/distancias

Distancia y tiempo reales desde un origen a una lista de centros, según el modo
de transporte. Se calcula por lotes y se cachea en el backend.

**Body**
```json
{
  "origin": { "lat": 37.178, "lng": -3.599 },
  "codigos": ["18700430", "18002991"],
  "mode": "driving"
}
```

`mode`: `driving` (coche) · `walking` (andando) · `bicycling` (bici) · `transit` (transporte público).

**200 OK**
```json
{
  "results": [
    { "codigo": "18700430", "status": "OK", "distance_m": 1786, "distance_text": "1,8 km", "duration_s": 529, "duration_text": "9 min" },
    { "codigo": "18002991", "status": "OK", "distance_m": 1242, "distance_text": "1,2 km", "duration_s": 384, "duration_text": "6 min" }
  ]
}
```

Errores: `400` si ningún código es válido o falla Google.

---

## POST /api/export

Genera un **CSV descargable** con los centros indicados, **en el orden recibido**
e incluyendo **todas las columnas del directorio de origen** (89 campos). El
fichero es UTF-8 con BOM (Excel lo abre con los acentos correctos) y separador
`;`.

Columnas de salida: `orden_preferencia` + (si se aportan datos de viaje)
`modo_transporte, tiempo_viaje, distancia_ruta, distancia_recta_km` + las 89
columnas originales (`curso, codigo, D_DENOMINA, …`).

**Body**
```json
{
  "mode": "driving",
  "items": [
    { "codigo": "18002991", "duration_text": "6 min", "distance_text": "1,2 km", "distancia_recta_km": 0.9 },
    { "codigo": "18700430", "duration_text": "9 min", "distance_text": "1,8 km", "distancia_recta_km": 1.4 }
  ]
}
```

Los campos de viaje de cada `item` son opcionales; si no se envían, no se
añaden esas columnas.

**200 OK** — `Content-Type: text/csv; charset=utf-8`,
`Content-Disposition: attachment; filename="mis-centros-preferidos.csv"`.

Errores: `400` si ningún código es válido.

---

## POST /api/lookup

Resuelve una lista de **códigos de centro** a sus nombres y datos básicos, en el
mismo orden. Útil para convertir un listado de códigos (p. ej. de una
adjudicación) en nombres legibles. Tolera el cero inicial perdido (`4000018` →
`04000018`).

**Body**
```json
{ "codigos": ["04000018", "4000018", "99999999"] }
```

**200 OK**
```json
{
  "total": 3,
  "encontrados": 2,
  "items": [
    { "codigo": "04000018", "encontrado": true, "nombre": "Joaquín Tena Sicilia", "denominacion": "Colegio de Educación Infantil y Primaria", "municipio": "Abla", "provincia": "Almería", "titularidad": "Público" },
    { "codigo": "04000018", "encontrado": true, "nombre": "Joaquín Tena Sicilia", "municipio": "Abla", "provincia": "Almería", "titularidad": "Público" },
    { "codigo": "99999999", "encontrado": false }
  ]
}
```
