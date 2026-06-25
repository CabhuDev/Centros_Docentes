# Changelog

Todos los cambios destacables de **Centros Docentes de Andalucía** se anotan en
este fichero.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).
Las fechas son `AAAA-MM-DD`. Tipos de cambio: **Añadido**, **Cambiado**,
**Corregido**, **Eliminado**, **Seguridad**.

## [Sin publicar]

## [3.0.0] - 2026-06-25

Reescritura completa del proyecto a un stack moderno (FastAPI + React/Vite +
Docker) que **sustituye por completo** la versión anterior del repositorio
(frontend en JavaScript vanilla, curso 2024). El árbol de ficheros se reemplaza
íntegramente; la historia previa se conserva enlazada en el repositorio.

### Añadido
- Backend **FastAPI**: filtros (provincia, municipio, titularidad,
  etapa/enseñanza concreta), orden por cercanía (haversine + Google Distance
  Matrix con caché), `GET /api/centros`, `/meta`, `/geocode`, `/distancias`,
  `/export` (CSV con todos los campos de origen) y `/lookup` de códigos.
- Frontend **React + Vite** con sistema de diseño propio (estilo «Syllabus»,
  documentado en `frontend/DESIGN.md`): mapa Leaflet, preferencias marcables (★)
  reordenables y exportables, y pestaña «Buscar / Listado» (incluye el PDF del
  concurso de traslados).
- Despliegue con **Docker Compose** (dev / prod / tests) y suite de tests pytest.
- **Capa de opiniones de profesorado (`info_extra`)** por centro.
  - Nuevo `scripts/build_info_extra.py`: cruza el Excel manual de opiniones
    (`datos/Centros Andalucia drive.xlsx`) con los centros (por código →
    nombre+municipio → nombre+provincia) y genera `datos/info_extra_centros.csv`
    (dato limpio, versionable) y `datos/info_extra_revision.csv` (auditoría del
    saneado). Sanea nombres de personas y cotilleos personales; conserva los
    juicios sobre el centro.
  - `scripts/preprocess.py` mergea ese CSV y añade el campo `info_extra` a cada
    centro de `centros.json` (vacío si no hay). Se expone automáticamente en la
    API `GET /api/centros`.
  - El frontend muestra las notas en la ficha (`CenterCard.jsx`) solo si existen,
    con disclaimer *«Notas de la comunidad · opiniones no verificadas»* y estilo
    de marca (clases `.notas`, `.notas-aviso`, `.notas-texto` en `theme.css`).
  - Cobertura: 313 de 7.106 centros con opiniones incorporadas; 7 filas con
    opinión quedan sin cruzar (listadas al ejecutar el generador).

### Conocido
- `centros.json` (y su CSV de origen `datos/centros_24-25.csv`) tiene los acentos
  corruptos como carácter de reemplazo U+FFFD (`Almer�a`, `Joaqu�n`). El CSV ya
  viene así upstream; solo se corrige re-descargando el directorio de la Junta.

## Legacy (2024)

Versión original del repositorio (no etiquetada): frontend en JavaScript vanilla
(`frontend/js`, `frontend/css`) y un primer backend. Reemplazada por completo en
la 3.0.0. Su código permanece accesible en la historia del repo y en la rama
`v3.0`.
