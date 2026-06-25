# Frontend

SPA en **React 18 + Vite**. Diseño minimalista con paleta verde educativa.
Mapa con **Leaflet + OpenStreetMap** (tiles gratis); Google se usa solo en el
backend para geocodificar y calcular rutas.

## Estructura

```
frontend/
├─ index.html
├─ vite.config.js        Dev server + proxy /api → http://localhost:8000
├─ nginx.conf            Producción: sirve la SPA y hace de proxy a /api
├─ Dockerfile            Build con Node → servir con nginx
└─ src/
   ├─ main.jsx
   ├─ App.jsx            Estado global y orquestación
   ├─ api.js             Cliente del backend
   ├─ theme.css          Tema (variables de color, componentes)
   └─ components/
      ├─ StartPoint.jsx    Punto de partida (dirección, ubicación, clic en mapa)
      ├─ Filters.jsx       Provincia, municipio, titularidad, árbol etapas→enseñanzas
      ├─ MapView.jsx       Mapa Leaflet con marcadores
      ├─ CenterCard.jsx    Tarjeta de centro (métricas, badges, acciones)
      ├─ Preferences.jsx   Lista ordenable de preferencias + exportar
      └─ BuscarListado.jsx Pestaña: buscar por nombre/código + resolver listado de códigos
```

## Estado (App.jsx)

| Estado     | Qué es                                                            |
|------------|-------------------------------------------------------------------|
| `meta`     | Catálogo de filtros (de `/api/meta`).                             |
| `filters`  | `q, provincia, municipio[], titularidad, concertado, etapas[], ensenanzas[], match`. |
| `origin`   | Punto de partida `{ lat, lng, label }`.                          |
| `data`     | Resultado de `/api/centros` (`total`, `items`).                  |
| `drive`    | Mapa `codigo → { distance_m, duration_s, ... }` del modo elegido.|
| `mode`     | Modo de transporte: `driving \| transit \| bicycling \| walking`.|
| `sortBy`   | `tiempo \| ruta_km \| recta`.                                    |
| `favs`     | Preferencias (persisten en `localStorage`).                      |

## Flujo

1. Al cargar, pide `/api/meta` y rellena los filtros.
2. Cuando cambian filtros u origen (con *debounce* de 300 ms), pide `/api/centros`.
3. Si hay origen, pide `/api/distancias` para todos los centros devueltos según
   `mode` y guarda tiempos/distancias en `drive` (el backend trocea en paralelo).
4. La lista se reordena en cliente según `sortBy`.
5. ★ añade el centro a **preferencias**; se pueden reordenar y **descargar en
   CSV** (`POST /api/export`) en ese orden y con todos los campos del directorio.

## Pestañas

- **Por cercanía**: la vista principal (filtros + mapa + resultados + preferencias).
- **Buscar / Listado** (`BuscarListado.jsx`): dos utilidades —
  *Buscar centro* por nombre o código (usa `/api/centros?q=`), y *Resolver
  listado*, que extrae los códigos de centro de un texto pegado o de un fichero
  **`.txt`, `.csv`, `.xlsx` o `.pdf`** (incluido el PDF del concurso de
  traslados), llama a `/api/lookup` y muestra los nombres, con opciones de
  copiar, descargar `.txt` o descargar el CSV completo.

  - PDF/Excel se leen en el navegador con `pdfjs-dist` y `xlsx`, **cargadas bajo
    demanda** (`import()` dinámico) para no inflar el bundle inicial.
  - La extracción busca números de 8 dígitos (rellena 7→8 para Almería) y los
    filtra por **prefijo de provincia** (04/11/14/18/21/23/29/41), de modo que
    ignora DNI, teléfonos y números de documento. Acepta el sufijo de tipo
    pegado (p. ej. `18700244C`).

## Filtro de enseñanzas

Las etapas se muestran como árbol: el chip selecciona la etapa (grueso) y, si
tiene varias modalidades, el botón `▾` despliega las **enseñanzas concretas**
(p. ej. *Bachillerato ordinario / para adultos / a distancia*). El conmutador
*Cualquiera / Todas* aplica a etapas y enseñanzas a la vez.

## Modo de transporte

El selector de iconos (🚗 🚌 🚲 🚶) en la cabecera de resultados cambia `mode`,
lo que recalcula las distancias/tiempos y ajusta las etiquetas y el enlace
"Cómo llegar" de cada tarjeta.

## Tema

Variables CSS en `theme.css` (`--green-600`, `--ink`, etc.). Para cambiar la
identidad de color basta con editar esas variables.

## Configuración

`VITE_API_BASE` (opcional): base de la API si el backend no está en el mismo
dominio. En dev y en la imagen de producción se deja vacío (el proxy resuelve).
