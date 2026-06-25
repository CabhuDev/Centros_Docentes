# Changelog

Todos los cambios destacables de **Centros Docentes de Andalucía** se anotan en
este fichero.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).
Las fechas son `AAAA-MM-DD`. Tipos de cambio: **Añadido**, **Cambiado**,
**Corregido**, **Eliminado**, **Seguridad**.

## [Sin publicar]

### Añadido
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

## [0.1.0] - 2024

### Añadido
- Buscador de centros docentes de Andalucía (curso 2024/2025, 7.106 centros)
  ordenados por **distancia y tiempo reales** según modo de transporte (coche,
  transporte público, bici, a pie) con Google Maps.
- Filtros por provincia, municipio, titularidad y etapa/enseñanza concreta.
- Preferencias marcables (★), reordenables, exportables a CSV con todos los
  campos del directorio de origen.
- Pestaña «Buscar / Listado»: búsqueda por nombre/código y resolución de listados
  de códigos (`.txt`, `.csv`, `.xlsx`, `.pdf`, incluido el PDF del concurso de
  traslados).
- Backend FastAPI + frontend React/Vite, despliegue con Docker Compose.
