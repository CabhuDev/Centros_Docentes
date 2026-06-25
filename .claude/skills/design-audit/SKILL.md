---
name: design-audit
description: >-
  Audita CSS/componentes del frontend contra el sistema de diseño de Centros
  Docentes (frontend/DESIGN.md) y lista las violaciones. Úsala antes de cerrar
  cualquier cambio visual, o cuando se pida revisar que la UI "es de marca".
---

# design-audit

Revisa que el código frontend respeta `frontend/DESIGN.md`. Devuelve una lista de
violaciones concretas (archivo + línea + qué regla rompe + arreglo propuesto). Si
no hay ninguna, dilo explícitamente: **"0 violaciones"**.

## Cómo auditar

1. Lee `frontend/DESIGN.md` (tokens y reglas vigentes) y luego los archivos a
   revisar (por defecto `frontend/src/theme.css`; también `*.jsx` con estilos
   inline o clases nuevas).
2. Busca cada infracción con Grep y razona sobre el resultado.

## Checklist de violaciones

Marca como violación todo lo siguiente:

- **Hex suelto** en CSS en vez de token. Detecta: `grep -nE '#[0-9a-fA-F]{3,6}'`
  en `theme.css` — solo deben aparecer hex **dentro del bloque `:root`** (la
  definición de tokens). Cualquier hex fuera de `:root` es violación.
- **Esquinas redondeadas:** `border-radius` con valor distinto de `0`/`var(--radius)`
  (excepto el `50%` legítimo del `.spinner` y de los marcadores de mapa).
  Detecta: `border-radius:` y `999px` / pills.
- **Sombras blandas:** `box-shadow` con `blur` (tercer valor > 0) o `rgba(...)`.
  Solo se permite la sombra dura `--shadow-press` / `--shadow-press-lg`
  (`Npx Npx 0`). Detecta: `box-shadow` + `blur`/`rgba`.
- **Color fuera de paleta:** cualquier color que no mapee a un token de la tabla
  de `DESIGN.md`.
- **Fondo de página blanco:** `background` del `body`/contenedor de página a
  `#fff`/`white` en vez de `--paper`.
- **CTA no amarillo:** un `.btn` primario relleno de violeta/teal en vez de
  `--accent`.
- **Tipografía desviada:** `font-family` que no sea `var(--sans)`/`var(--mono)`;
  tamaños/pesos fuera de la escala documentada; datos (códigos/tiempos/distancias)
  que NO van en `--mono`.
- **Gradientes:** cualquier `gradient(`.
- **Framework CSS:** import/uso de Tailwind, Bootstrap, Material, etc., o nuevas
  dependencias de estilos en `package.json`.

## Salida

Formato por hallazgo:

```
[archivo:línea] REGLA — descripción breve
  ↳ arreglo: <token o cambio concreto>
```

Cierra con un veredicto: **"0 violaciones"** o **"N violaciones — corregir antes de mergear"**.
No corrijas tú salvo que te lo pidan: este skill informa; aplicar es trabajo del
agente `disenador-ui` con `design-apply`.
