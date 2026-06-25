# Centros Docentes · Investigación de mercado y competidores

> Mercado: **España**. Nicho: herramientas que ayudan a docentes a **elegir y ordenar destinos** (concurso de traslados, colocación de efectivos/interinos, adjudicación de oposiciones), especialmente **por cercanía / tiempo de viaje**.
> Fecha del análisis: **junio 2026**. Fuentes verificadas al final de cada bloque.
> Conclusión corta: **el cálculo por cercanía ya es un commodity gratuito** (incluso en Andalucía). Monetizar como SaaS de pago a docentes es **poco viable**; el valor real está en **features que nadie cubre**, en **B2B** y en **ingreso indirecto**. Ver §7–§8.

---

## 1. Panorama en una frase

Existen varias herramientas como la nuestra, casi todas **gratuitas** (open source, donativo, o gancho de academia/sindicato). En **Andalucía ya hay un competidor directo gratuito (EduGeo)** que calcula tiempo en coche a todos los centros con vacantes oficiales. El mercado está **fragmentado por comunidad autónoma** y **no tiene un producto de pago consolidado** centrado en ordenar por cercanía.

---

## 2. Competidores DIRECTOS e INDIRECTOS (ordenar centros por cercanía)

| Herramienta | Qué hace exactamente | CCAA | Motor de rutas/datos | Precio | Modelo de negocio | Plataforma | Activa | Amenaza |
|---|---|---|---|---|---|---|---|---|
| **EduGeo Andalucía** · [er-gom.com](https://er-gom.com/) | Distancia y **tiempo en coche** a todos los centros; ordena por tiempo/vacantes/alquiler; favoritos, notas, lista guardable; **plantilla orgánica y vacantes oficiales** del CGT | **Andalucía** | OpenRouteService + OpenStreetMap (rutas reales) | **Gratis** | Sin monetización visible | Web (con registro) | Sí (efectivos 2026) | 🔴 **Directo: es nuestra app, gratis, ya en Andalucía** |
| **Mi Destino Docente** · [midestinodocente.es](https://midestinodocente.es/) | Destinos más cercanos + tiempos/distancias; **calculadora de baremo**; **posición en bolsa de interinos**; opiniones de centros; **alquiler docente** y **carpooling**; foro y newsletter | Multi-CCAA (España) | Base propia (+48.000 localidades, "120M rutas") | **Freemium** ([Mi Suscripción](https://www.midestinodocente.es/mi-suscripcion/)) — **precio NO público** | Suscripción + servicios anexos (alquiler, ads probable) | Web | Sí (2026) | 🔴 **El más completo y nacional** |
| **Mis Centros Educativos** · [miscentroseducativos.com](https://miscentroseducativos.com/) | Tiempo de viaje (coche/bici/bus/pie), filtros (DAT, bilingüe, difícil desempeño), favoritos ordenables, **export Excel** | Madrid | No especificado | Gratis (cuenta) | Sin modelo explícito | Web | Sí (2025) | 🟠 Indirecto (otra CCAA) |
| **miconcursillo.es** · [miconcursillo.es](https://miconcursillo.es/) | Tiempos de viaje a cada centro, filtros, **export de preferencias** (concursillo/interinos) | Madrid | No especificado | Gratis | No documentado | Web | Sí | 🟠 Indirecto |
| **Centros Educativos de Galicia** · [centroseducativos.gal](https://centroseducativos.gal/) | Ordena por nombre/distancia/**tiempo en coche**; export texto/PDF/portapapeles; pensada para CXT y CADP | Galicia | Cálculo de rutas propio | Gratis · **open source (AGPL)**, GitHub | Ninguno | Web | Sí | 🟠 Indirecto |
| **Mapa centros (s-nt-s)** · [s-nt-s.github.io/centros](https://s-nt-s.github.io/centros/concursillo/) | Mapa que ordena por **proximidad a un punto**; filtros, listas, **export multiformato + SQLite**; variante EOI | Madrid | Mapa interactivo | Gratis · **GPL, donativos** | Donaciones | Web | Sí (2026-27) | 🟠 Indirecto |
| **Mapa Adjudicaciones Andalucía** · [mapavacantesandalucia.es](https://www.mapavacantesandalucia.es/) | Mapa **histórico de vacantes** por especialidad/provincia/cuerpo (no calcula rutas) | Andalucía | Datos Consejería vía CSIF | Gratis | Donativo ("café") | Web | Sí (25/26) | 🟢 Complementario |
| **SIPRI Andalucía (privado)** · [sipriandalucia.es](https://sipriandalucia.es/) | Buscador de adjudicaciones + **"El Oráculo"** (predice por dónde va la bolsa) + histórico | Andalucía | Datos públicos SIPRI | Gratis | No documentado | Web | Sí (jun-2026) | 🟢 Complementario (predicción) |
| **sipri.es** · [sipri.es](https://sipri.es/) | Newsletter de avisos de convocatorias/adjudicaciones, guías, tutoriales | Andalucía/España | — | Gratis | No documentado | Web | Sí | 🟢 Complementario (info) |

**Lectura:** el "ordenar por tiempo de coche" **no es diferenciador** — EduGeo ya lo regala en Andalucía con datos oficiales y motor OSM (sin coste por llamada). Mi Destino Docente cubre lo mismo a nivel nacional y añade servicios.

---

## 3. Plataformas OFICIALES de adjudicación (contexto: el trámite real)

Son gratuitas (administración) y solo **gestionan la petición**, no ayudan a decidir el orden óptimo → ahí está el dolor que una herramienta de terceros resuelve.

| Plataforma | CCAA | Función |
|---|---|---|
| **SIPRI** · [sipri.juntadeandalucia.es](https://sipri.juntadeandalucia.es/sipri/inicio/) | Andalucía | Adjudicación de destinos provisionales/interinidades ("colocación de efectivos"), 2 convocatorias/semana |
| **PADI** · [comunidad.madrid](https://www.comunidad.madrid/servicios/educacion/profesorado-interino) | Madrid | Asignación de interinos; orden de preferencia online |
| **Adjudicación continua** · [ceice.gva.es](https://ceice.gva.es/es/web/rrhh-educacion/adjudicacion-continua) | C. Valenciana | Peticiones telemáticas, adjudicaciones martes/jueves |
| **AIDPRO/AIDPRA** · [JCyL](https://www.tramitacastillayleon.jcyl.es/) | Castilla y León | Adjudicación informatizada de destinos provisionales |

---

## 4. Calculadoras de baremo (no ordenan centros, pero son el otro gran bloque)

Todas **gratuitas**; el negocio es la **captación** (academia) o la **afiliación** (sindicato).

| Recurso | Detrás | Modelo | Cuota/precio |
|---|---|---|---|
| [Campus Educación](https://www.campuseducacion.com/baremo-concurso-traslados) | Academia (Albacete) | Calculadora gratis → **vende cursos/másteres** | Curso de pago |
| [FE-CCOO](https://calculadoras.fe.ccoo.es/) | Sindicato | Incluido / gancho de afiliación | Cuota CCOO **5–17 €/mes** (por tramos) |
| [CSIF](https://www.csif.es/es/portada/andaluciaeducacion/categoria/traslados) | Sindicato | Calculadora + dossier + videotutoriales; asesoría a afiliados | Cuota CSIF **~11,5 €/mes** |
| ANPE (territoriales) | Sindicato | Excel de baremo + guías; asesoría a afiliados | Cuota ANPE **80 €/año** |
| SIDI | Sindicato | **Excel descargable** de baremo | Cuota |

**Academias grandes (canal y posibles socios B2B):** Magister, CEDE, CEN, ECOEM, TecnosZubia.

---

## 5. Apps de opositores (para delimitar el nicho)

OpositaTest, Meludus, OpositApp, Studeam, Opospills, Opocoach… → **solo estudio/tests/productividad**. **Ninguna** toca elección de destinos. Confirma que nuestro nicho es **otro** (y está mucho menos poblado).

---

## 6. Mercado y estacionalidad

- **Profesorado no universitario España:** 784.425 (569.705 públicos), curso 23-24 ([MEFP](https://www.educacionfpydeportes.gob.es/servicios-al-ciudadano/estadisticas/no-universitaria/profesorado/estadistica/2023-2024-rd.html)).
- **Interinidad:** ~24-25% (1 de cada 4). Andalucía **~22.500 interinos** activos (dic-2023); **~16.905 puestos** adjudicados en un solo trimestre.
- **Oposiciones Andalucía:** **38.222 aspirantes / 7.998 plazas (2025)**; 21.366 / 5.047 (2026) ([Junta](https://www.juntadeandalucia.es/presidencia/portavoz/educacion/207662/)).
- **Concurso de traslados:** estatal **bienal**; nº de participantes **no se publica**.
- **Dos picos de demanda al año:**
  - **Traslados:** convocatoria **noviembre** → destinos **mayo**.
  - **Oposiciones + interinos:** examen **junio** → adjudicaciones **verano (jul–sep)** ← **pico de máxima necesidad de elegir destino por cercanía.**
- **Canales (go-to-market):** Telegram (Docentes Andalucía, OpositaJA, Bolsas Docentes, Maestros25), grupos Facebook (Interinos de Andalucía, Maestros/as Andaluces), foros (foroopositores.com, maestros25), webs sindicales y portales SIPRI.

---

## 7. Datos oficiales y legalidad (lo que condiciona el producto)

| Asunto | Estado | Implicación |
|---|---|---|
| **Directorio centros Andalucía** ([datos abiertos](https://www.juntadeandalucia.es/datosabiertos/portal/dataset/directorio-de-centros-docentes-de-andalucia)) | CSV con coordenadas, **CC BY 4.0** | ✅ **Uso comercial permitido** citando fuente. Base legal sólida (ya la usamos). |
| **RCD estatal (MEFP)** | Solo consulta web, sin licencia clara | ⚠️ No apoyarse en él; usar datasets autonómicos (ojo: algunas CCAA son **CC BY-NC**, sin uso comercial). |
| **datos.gob.es / RISP** (Ley 37/2007, 18/2015) | Permite reutilización **comercial** | ✅ Citar fuente, no desnaturalizar. |
| **Google Maps – Distance Matrix** ([policies](https://developers.google.com/maps/documentation/distance-matrix/policies)) | **Prohíbe** cachear/almacenar tiempos y **mostrarlos sobre mapa NO-Google** | 🔴 **Nuestra app mezcla distancias de Google con mapa Leaflet/OSM → incumple TOS.** Migrar a **OpenRouteService/OSRM/Valhalla** (como EduGeo): quita el riesgo **y** el coste por llamada. |

---

## 8. Viabilidad de monetización — lectura honesta

**Como SaaS de pago a docentes individuales: poco viable.** Razones:
- El núcleo (ordenar por cercanía) está **regalado**, incluso en Andalucía (EduGeo) y a nivel nacional (Mi Destino Docente, freemium).
- Uso **estacional** (2 picos/año) → mala recurrencia para una suscripción.
- **Disposición a pagar baja**: el docente ya paga (si acaso) cuota sindical (que incluye asesoría humana) o curso de academia; "ordenar centros" no se percibe como algo de pago.
- Competidores gratis **subvencionados por vocación** (open source) o por **otros ingresos** (academia/alquiler) → difícil competir cobrando por la herramienta.

**Conclusión:** no conviene apostar el proyecto a una cuota. Conviene **maximizar valor por otras vías** (§9).

---

## 9. VALOR EXTRA — dónde sí hay leverage

Tres palancas, de menor a mayor solidez:

### A) Features que NADIE cubre (única vía con disposición real a pagar, y baja)
1. **Generador de la PETICIÓN EN FORMATO OFICIAL** (lista de códigos lista para volcar en la sede telemática). **Nadie lo hace**; todas exportan Excel/PDF genérico. Es el dolor no resuelto.
2. **Simulador de adjudicación** ("con tu baremo + estas vacantes, te tocaría X"). No existe en versión predictiva (lo más cercano, "El Oráculo", es orientativo).
3. **Resolutor de códigos** (PDF/Excel del concurso → nombres) — ya lo tenemos y es **poco común**: úsalo como **gancho/USP**.

→ Si se cobra, que sea **micropago por convocatoria (~4,99 €)** que desbloquee *petición oficial + simulador* durante la campaña. Nunca como barrera al cálculo de cercanía (ese, gratis).

### B) B2B / indirecto (lo más robusto y defendible)
- **White-label para academias** (Magister, CEDE, ECOEM, TecnosZubia): tu herramienta con su marca como valor añadido a sus alumnos → licencia por temporada. **Aquí sí hay presupuesto.**
- **Licencia a un sindicato**: les falta producto digital; ofrecérselo como servicio al afiliado.
- **Afiliación/marketplace** (modelo Mi Destino Docente): alquiler entre docentes, carpooling, **referidos a academias** → ingreso sin cobrar al usuario.
- **Ads estacionales** en los dos picos (academias, editoriales, seguros, alquiler).

### C) Valor NO monetario (subestimado, pero real)
- **Coste marginal ≈ 0** si migras a routing OSM → puedes mantenerlo **gratis para siempre** sin sangrar dinero. Eso permite **ganar reputación y usuarios**, que es lo que habilita A) y B).
- **Pieza de portfolio / CV técnico** de primer nivel (full-stack + datos abiertos + geo): valor profesional propio.
- **Bien público útil** a miles de docentes andaluces: tracción y comunidad, que tienen valor aunque no se facture.

---

## 10. Recomendación

1. **No** montar muro de pago sobre el cálculo de cercanía. **Sí** hacerlo gratis y mejor que EduGeo en lo accesorio (UX, resolutor de códigos, multi-CCAA).
2. **Migrar el motor de rutas a OSM** (OpenRouteService/OSRM): elimina el riesgo legal de Google y el coste → sostenible gratis.
3. Construir el **diferenciador real**: **generador de petición oficial** + (a medio plazo) **simulador de adjudicación**. Si algo se cobra, micropago por convocatoria; si no, queda como gancho de tracción.
4. **Explorar B2B** con una academia andaluza como primer cliente (la vía con presupuesto real).
5. **Go-to-market Andalucía primero**, lanzando antes de los picos (mayo / verano), difundiendo en Telegram/Facebook/foros docentes.
6. Tratar el proyecto como **activo de reputación + base para B2B**, no como suscripción B2C.

---

## Fuentes
Ver enlaces inline. Principales: [EduGeo](https://er-gom.com/) · [Mi Destino Docente](https://midestinodocente.es/) · [miscentroseducativos](https://miscentroseducativos.com/) · [centroseducativos.gal](https://centroseducativos.gal/) · [s-nt-s](https://s-nt-s.github.io/centros/concursillo/) · [mapavacantesandalucia](https://www.mapavacantesandalucia.es/) · [sipriandalucia](https://sipriandalucia.es/) · [Dataset Andalucía CC BY 4.0](https://www.juntadeandalucia.es/datosabiertos/portal/dataset/directorio-de-centros-docentes-de-andalucia) · [datos.gob.es aviso legal](https://datos.gob.es/es/aviso-legal) · [Google Distance Matrix policies](https://developers.google.com/maps/documentation/distance-matrix/policies) · [MEFP profesorado 23-24](https://www.educacionfpydeportes.gob.es/servicios-al-ciudadano/estadisticas/no-universitaria/profesorado/estadistica/2023-2024-rd.html)

## Limitaciones
- Precio de **Mi Destino Docente** no verificado (tras login).
- **Nº de participantes del concurso de traslados** no publicado (cualquier cifra sería estimación).
- Tamaños de grupos de Telegram/Facebook no accesibles públicamente.
- El apartado legal es **orientativo, no asesoramiento jurídico**: revisar licencia de cada dataset y términos vigentes de Google antes de lanzar.
