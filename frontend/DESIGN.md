# Sistema de diseño · Centros Docentes

> **Fuente única de verdad del diseño.** Todo cambio visual de la app se rige por
> este documento. Si algo que vas a construir no encaja aquí, primero actualiza
> este archivo (y sus tokens en `src/theme.css`), luego implementa. No hay diseño
> "a ojo": hay tokens.
>
> Lo mantiene el agente **`disenador-ui`** (`.claude/agents/disenador-ui.md`) con
> las skills `design-audit` y `design-apply`.

---

## 1. Marca y principios

Centros Docentes adopta un lenguaje **editorial-brutalista** ("crema-papel de
revista + sans geométrica"), tomado del sistema *Syllabus*. La sensación es de
**herramienta seria, impresa y de confianza**: un directorio público con carácter,
no una web SaaS más.

Cinco principios irrenunciables:

1. **El lienzo es crema, nunca blanco.** El fondo `--paper #fffcf7` es la identidad.
   El blanco puro se reserva para tarjetas elevadas sobre la crema.
2. **La estructura la dibujan bordes de tinta, no sombras.** Borde `1px solid --ink`
   en todo lo que es un contenedor. Sin sombras blandas difuminadas.
3. **El amarillo es la única voz alzada.** `--accent #fae59b` solo en botones de
   acción (CTA) y acentos pequeños (4–8px). Nunca como fondo de zonas grandes.
4. **Esquinas rectas siempre.** `border-radius: 0`. Nada de pills ni cantos redondeados.
5. **Los datos hablan en monoespaciada.** Códigos de centro, tiempos, distancias y
   cifras van en `--mono`: es la "voz técnica" del directorio.

El **teal** `--teal #19615c` es el color institucional de apoyo: zonas a sangre
(cabecera de mapa, franjas) y acentos de dato. Aporta contraste tonal sin cajas.

---

## 2. Tokens

Definidos en `src/theme.css` bajo `:root`. **Nunca escribas un hex suelto en el
CSS**: usa siempre una variable. Si necesitas un color que no existe, añádelo aquí
primero.

### Color

| Token | Hex | Uso |
|---|---|---|
| `--paper` | `#fffcf7` | Fondo de página (lienzo crema). |
| `--surface` | `#ffffff` | Tarjetas/paneles elevados sobre la crema. |
| `--ink` | `#0d0129` | Texto principal y **todos los bordes**. |
| `--ink-soft` | `#4a4560` | Texto secundario. |
| `--ink-faint` | `#7c7790` | Texto terciario, hints, labels apagados. |
| `--accent` | `#fae59b` | **Solo CTAs y acentos pequeños.** |
| `--accent-soft` | `#fdf6dd` | Tinte amarillo para fondos sutiles (chip `code`, foco). |
| `--teal` | `#19615c` | Color institucional: zonas a sangre, dato destacado. |
| `--teal-tint` | `#e6efee` | Fondo suave teal (origin-pill, badges de etapa). |
| `--danger` | `#9e2b25` | Errores, quitar, marcadores de origen alternos. |
| `--danger-tint` | `#f7e7e5` | Fondo suave de error (p. ej. fila "no encontrado"). |

Prohibido: gradientes, blanco puro como **fondo de página**, cualquier color fuera
de esta tabla.

### Tipografía

| Token | Familia | Rol |
|---|---|---|
| `--sans` | `'Space Grotesk', 'Inter', system-ui, sans-serif` | Todo el texto de interfaz. Sans geométrica. |
| `--mono` | `'JetBrains Mono', 'IBM Plex Mono', ui-monospace, monospace` | **Datos**: códigos, tiempos, distancias, cifras. |

- Pesos: **400** (cuerpo/labels), **500** (subtítulos/énfasis), **700** (titulares y
  texto de botón). La jerarquía nace de los **saltos de tamaño**, no del tracking.
- Escala (px): `12 · 13 · 14 · 16 · 20 · 26 · 34`. Titulares grandes saltan, no crecen poco a poco.
- Texto de botón y micro-labels en **mayúsculas** con `letter-spacing: .04em`.
- Las fuentes se cargan vía `<link>` en `index.html` (Google Fonts). Las fuentes
  **no son** un framework CSS: la restricción "sin frameworks CSS" se respeta.

### Espaciado, bordes, sombra

| Token | Valor | Uso |
|---|---|---|
| base | `8px` | Ritmo: 4 · 8 · 12 · 16 · 24 · 32 · 48. |
| `--border` | `1px solid var(--ink)` | Borde estructural universal. |
| `--border-strong` | `2px solid var(--ink)` | Separadores de marca (topbar, foco). |
| `--radius` | `0` | Global. No se redondea nada. |
| `--shadow-press` | `3px 3px 0 var(--ink)` | Sombra **dura desplazada**, efecto "pegatina pulsable". CTAs. |
| `--shadow-press-lg` | `5px 5px 0 var(--ink)` | Hover de tarjetas/CTA: la pieza "salta". |

Solo existe esta sombra. **Sin `blur`, sin multicapa, sin sombras suaves.**

---

## 3. Especificación por componente

Las clases ya existen en el código; aquí se fija su apariencia. Mantén los nombres.

- **`.topbar`** — Fondo crema, `border-bottom: var(--border-strong)`. Título 700.
  `.logo` = cuadrado `--ink` con glifo crema y punto/acento amarillo. `.sub` en `--mono`.
- **`.tabs` / `.tabs button`** — Rectangulares (radius 0), borde ink. Activo (`.on`):
  relleno `--ink`, texto crema. Inactivo: fondo crema, texto ink.
- **`.btn` (primario)** — Relleno `--accent`, borde ink, texto ink **700 mayúsculas**,
  `box-shadow: var(--shadow-press)`. `:hover` → `--shadow-press-lg` y `translate(-2px,-2px)`.
  `:active` → sin sombra y `translate(0,0)` (se hunde). `:disabled` → relleno `--accent-soft`, sin sombra.
- **`.btn.ghost`** — Transparente, borde ink, texto ink, sin sombra. Hover: fondo `--accent-soft`.
- **`.btn.sm`** — Mismo lenguaje, menor padding/tamaño.
- **`.chip` / `.badge`** — Etiquetas **rectangulares** con borde ink, fondo crema/transparente.
  Activo (`.chip.on`): relleno `--ink`, texto crema. `.badge.tit` = tinte `--teal-tint`,
  texto teal, borde ink. `.badge.tit.concert` = tinte `--accent-soft`. `.code` = `--mono`
  sobre `--accent-soft`, borde ink.
- **`.seg` / `.mode-seg`** — Control segmentado con borde ink, divisiones a 1px ink.
  Segmento activo: relleno `--ink` (texto crema) o, en `.mode-seg`, tinte `--accent-soft`
  con barra inferior `--ink`.
- **`.card` / `.panel` / `.lk-row`** — Superficie `--surface`, borde ink, radius 0,
  sin sombra en reposo. `.card:hover` → `--shadow-press-lg` + `translate(-3px,-3px)`.
  `.card.fav` → barra/acento `--accent` a la izquierda. `.lk-row.missing` → tinte `--danger`.
- **`.metric .v`** — En **`--mono`**, color `--ink`. El tiempo de viaje (`.v.car`) en `--teal`.
  `.metric .k` = micro-label mayúsculas `--ink-faint`.
- **`.input` / `select` / `textarea`** — Fondo blanco, borde ink, radius 0. Foco:
  borde ink + anillo amarillo `box-shadow: 0 0 0 3px var(--accent)`.
- **`.origin-pill`** — Rectangular, fondo `--teal-tint`, borde ink; `.dot` = punto `--accent`.
- **`.notas` / `.notas-aviso` / `.notas-texto`** — Bloque de "Notas de la comunidad"
  dentro de `.card`: opiniones de profesorado **subjetivas y no verificadas**, no dato
  oficial. Contenedor con borde ink y fondo `--accent-soft` (tinte amarillo = nota al
  margen, lo separa de la superficie blanca del centro). `.notas-aviso` = micro-label
  mayúsculas `--ink-faint` con `.dot` de acento `--accent` (8px) y separador inferior
  `1px` ink; deja claro que es un aviso. `.notas-texto` = prosa en `--sans` `--ink-soft`
  (es texto de interfaz, no un dato → no va en `--mono`). Sin sombra (contenido secundario).
- **`.divider`** — `1px` ink (línea de marca).
- **Mapa (`.marker-pin`)** — Marcador de centro: cuadrado/teardrop `--ink`, borde crema.
  `.marker-pin.origin` = `--accent` con borde ink. `.leaflet-container` fondo `--teal-tint`.
- **`.spinner`** — Aro `--teal-tint` con cabeza `--ink`/`--teal`.
- **`.empty` / `.hint` / `.error`** — Texto `--ink-faint` (error en `--danger`), sin caja.

---

## 4. Do / Don't

**Do**
- Lienzo crema como identidad; blanco solo para tarjetas elevadas.
- Bordes 1px de tinta para estructurar; esquinas rectas en todo.
- Amarillo solo en CTAs y acentos ≤8px, siempre con sombra dura.
- Datos en monoespaciada (códigos, tiempos, distancias).
- Teal para franjas a sangre y dato destacado.
- Usar **solo tokens**; añadir el token aquí antes de usar un color nuevo.

**Don't**
- ❌ Blanco puro como fondo de página.
- ❌ `border-radius` > 0 (nada de pills ni cantos suaves).
- ❌ Sombras blandas / difuminadas / multicapa / gradientes.
- ❌ CTAs rellenos de violeta o teal (el CTA es amarillo).
- ❌ Cambiar de tipografía o inventar pesos/tamaños fuera de la escala.
- ❌ Hex sueltos en el CSS. ❌ Frameworks CSS (Tailwind, Bootstrap, etc.).

---

## 5. Desviaciones conocidas

- **Emojis de modo de transporte** (🚗 🚌 🚲 🚶) y algún icono funcional puntual se
  toleran por pragmatismo. El ideal del estilo son line-icons planos de 1–1.5px en
  tinta; migrar a SVG queda como mejora futura. Cualquier emoji nuevo debe justificarse.

---

## 6. Mantenimiento

1. Antes de tocar UI, **lee este documento**.
2. Cambia apariencia **solo** vía `src/theme.css` y **solo** con tokens.
3. ¿Color/medida nueva? Primero token aquí (tabla) y en `:root`, luego úsalo.
4. Nunca añadas un framework CSS ni una dependencia de estilos.
5. Al evolucionar el sistema, **actualiza este archivo en el mismo cambio**.
6. Verifica con la skill `design-audit` (debe dar 0 violaciones).
