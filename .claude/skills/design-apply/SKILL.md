---
name: design-apply
description: >-
  Receta para construir o reestilar UI de Centros Docentes conforme al sistema de
  diseño (frontend/DESIGN.md). Cheat-sheet de tokens y patrones por tipo de
  elemento. Úsala al crear/cambiar componentes o estilos del frontend.
---

# design-apply

Guía para implementar UI que **ya nace de marca**. Trabaja siempre sobre
`frontend/src/theme.css` con tokens; no metas hex sueltos ni frameworks.

## Antes de empezar

1. Lee `frontend/DESIGN.md` (la spec por componente fija cómo debe verse cada cosa).
2. Comprueba si la clase ya existe en `theme.css`: reestilar suele ser cambiar CSS,
   no JSX.

## Cheat-sheet de tokens

```
Fondo página     background: var(--paper)        /* crema, nunca blanco */
Tarjeta/panel    background: var(--surface); border: var(--border)
Texto            color: var(--ink) / --ink-soft / --ink-faint
Borde            border: var(--border)           /* 1px ink */  · var(--border-strong) 2px
Esquinas         border-radius: var(--radius)    /* = 0 */
Sombra           box-shadow: var(--shadow-press) /* hover: --shadow-press-lg */
CTA              background: var(--accent) + sombra dura + texto ink 700 mayúsculas
Acento ≤8px      var(--accent)                   /* puntos, barras de fav */
Institucional    var(--teal) / fondo var(--teal-tint)
Error/quitar     var(--danger)
Texto interfaz   font-family: var(--sans)
Datos            font-family: var(--mono)        /* códigos, tiempos, distancias, cifras */
```

## Patrones por elemento

- **Botón de acción** → `.btn`: amarillo, borde ink, `--shadow-press`, texto 700
  mayúsculas; `:hover` levanta (`--shadow-press-lg` + translate), `:active` se hunde.
- **Botón secundario** → `.btn.ghost`: transparente, borde ink, sin sombra.
- **Etiqueta/tag** (etapa, titularidad, código) → rectangular, borde ink, radius 0.
  Estado activo: relleno ink, texto crema. Dato/código → `--mono` sobre `--accent-soft`.
- **Tarjeta/contenedor** → `--surface` + borde ink, radius 0, sin sombra en reposo;
  hover opcional `--shadow-press-lg`. Destacado → barra/acento `--accent` a la izquierda.
- **Input/select/textarea** → blanco, borde ink, radius 0; foco = anillo amarillo
  `box-shadow: 0 0 0 3px var(--accent)`.
- **Cifra/dato** → `--mono`, peso 700; tiempo de viaje en `--teal`; micro-label
  encima en mayúsculas `--ink-faint`.
- **Franja/cabecera de marca** → fondo `--teal` con texto crema, o crema con borde
  `--border-strong` inferior.
- **Control segmentado** → contenedor con borde ink, divisiones 1px ink; activo
  relleno ink (texto crema).

## Reglas duras

- Solo tokens. ¿Falta uno? Añádelo a la tabla de `DESIGN.md` **y** a `:root`, luego úsalo.
- `border-radius: 0` salvo `50%` de spinner/marcadores.
- Solo sombra dura (sin blur). Solo el amarillo de `--accent` como "voz alzada".
- Datos en `--mono`. Sin gradientes. Sin frameworks CSS.

## Al terminar

- Si añadiste o cambiaste algo del sistema, **actualiza `frontend/DESIGN.md`** en
  el mismo cambio.
- Pasa la skill `design-audit` sobre lo que tocaste; corrige hasta 0 violaciones.
