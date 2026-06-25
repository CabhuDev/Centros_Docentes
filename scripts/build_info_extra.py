"""
Genera la capa de "info extra" de los centros a partir del Excel manual con
opiniones y experiencias de profesorado (columna INFO EXTRA IES, e INFO 2024).

  Entrada : datos/Centros Andalucia drive.xlsx   (una hoja por provincia)
  Salidas :
    datos/info_extra_centros.csv    -> codigo,info_extra   (limpio, versionable)
    datos/info_extra_revision.csv   -> auditoria: original vs saneado + metodo

Cruza cada fila del Excel con backend/app/data/centros.json:
  1) por codigo de centro (8 digitos, exacto)
  2) si no hay codigo, por nombre + municipio normalizados

Saneado de contenido sensible
-----------------------------
El texto se conserva LITERAL salvo nombres de personas y cotilleos personales
("novio de...", "hermana de...", atribuciones tipo "Ismael (Almeria):"...), que
se eliminan. Los juicios sobre el centro ("MALO", "buen centro"...) se mantienen.
Las entradas con nombre propio se tratan una a una en OVERRIDES; ademas se aplica
una pasada generica y, como red de seguridad, se marca en el CSV de revision
cualquier fila donde quede un nombre de la lista NOMBRES_VIGILADOS.

Uso:
  python scripts/build_info_extra.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "datos" / "Centros Andalucia drive.xlsx"
CENTROS_JSON = ROOT / "backend" / "app" / "data" / "centros.json"
OUT_CSV = ROOT / "datos" / "info_extra_centros.csv"
OUT_REVISION = ROOT / "datos" / "info_extra_revision.csv"

# --------------------------------------------------------------------------
# Normalizacion
# --------------------------------------------------------------------------

def _fold(s: str) -> str:
    """A ASCII en minusculas (sin acentos ni el caracter de reemplazo)."""
    if not isinstance(s, str):
        return ""
    s = s.replace("�", "")  # centros.json tiene acentos rotos como U+FFFD
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.lower()


def norm_key(s: str) -> str:
    """Clave estable para comparar textos: solo alfanumerico + espacios."""
    return re.sub(r"[^a-z0-9]+", " ", _fold(s)).strip()


_NOMBRE_RUIDO = re.compile(
    r"\b(i\.?\s*e\.?\s*s\.?o?|c\.?\s*e\.?\s*i\.?\s*p\.?|colegio|instituto|"
    r"de educacion secundaria|seccion)\b"
)


def norm_nombre(s: str) -> str:
    return re.sub(r"\s+", " ", _NOMBRE_RUIDO.sub(" ", norm_key(s))).strip()


def norm_codigo(v) -> str | None:
    digits = re.sub(r"\D", "", str(v)) if v is not None else ""
    return digits.zfill(8) if digits else None


# --------------------------------------------------------------------------
# Saneado de contenido sensible
# --------------------------------------------------------------------------
# Nombres propios detectados en el Excel; usados como red de seguridad para
# marcar en revision cualquier fila donde alguno sobreviva al saneado.
# Nota: "vilches" es un pueblo/IES (se usa como comparacion, "como Vilches"),
# no una persona; "eva" como subcadena genera falsos positivos -> fuera.
NOMBRES_VIGILADOS = [
    "ismael", "emilio", "melissa", "silvia", "sara", "lourdes",
    "alicia", "yolanda", "luisa", "hugo", "calata", "jose antonio",
    "navarro", "calahorro", "maria del mar", " ro ", "porrero", "amparo",
]

# Saneado explicito, entrada por entrada, de las filas con nombres propios.
# Clave = norm_key(texto_original_combinado); valor = texto ya saneado.
# El texto saneado conserva el juicio sobre el centro y elimina personas.
_OVERRIDES_RAW: list[tuple[str, str]] = [
    ("Buen centro para Alicia y Malo para Lourdes (ella de los ultimos, prefiere Vilches)",
     "Para unos buen centro y para otros malo."),
    ("Buen centro para Alicia y Regular para Lourdes (ella de los ultimos, prefiere Vilches)",
     "Para unos buen centro y para otros regular."),
    ("Buen centro// Ismael (Almeria): En este centro estuve el curso 17-18: mucho profesorado mayor y muy muy muy muy mal rollo entre la directiva y las vacas sagradas. Antes no tenia 1o y 2o de ESO pero ya si. Muchos alumnos vienen de La Magdalena (el barrio chungo de Jaen) pero los alumnos que tuve y los que hubo ese ano eran buenos en el trato. Habia un solo profe de E.F. y daba tambien clase a los ciclos. Es un instituto viejo y enano (el patio parece el patio de una carcel) Es centro de compensatoria. Esta en pleno centro de Jaen. Hay clase por las tardes tambien. El claustro rondaba los 100 profes.",
     "Buen centro. En este centro estuve el curso 17-18: mucho profesorado mayor y muy mal rollo entre la directiva y las vacas sagradas. Antes no tenia 1o y 2o de ESO pero ya si. Muchos alumnos vienen de La Magdalena (el barrio chungo de Jaen) pero los alumnos que tuve y los que hubo ese ano eran buenos en el trato. Habia un solo profe de E.F. y daba tambien clase a los ciclos. Es un instituto viejo y enano (el patio parece el patio de una carcel). Es centro de compensatoria. Esta en pleno centro de Jaen. Hay clase por las tardes tambien. El claustro rondaba los 100 profes."),
    ("Bueno: el de Sara Navarro y Eva.", "Bueno."),
    ("MUY BUENO. Definitiva Ro.", "Muy bueno."),
    ("Grande, alumnado heterogeneo. Eq.Directivo competente (2020) (Jose Antonio). Lourdes dice MALO",
     "Grande, alumnado heterogeneo. Equipo directivo competente (2020). Para algunos, malo."),
    ("Ismael (Almeria): Estuve alli el curso pasado. Sin duda el mejor centro en el que he estado. Me pude desarrollar como profesional de una manera increible. Claustro poco numeroso (entre 35 y 45), muy, muy buen rollo. Son Comunidad de aprendizaje y la verdad que se lo curran mogollon. Todos los profes son super simpaticos y dinamicos: puedes contar con ellos para cualquier cosa. Par mi era el paraiso. El profe de E.F. es mayor pero esta lejos de jubilarse. Aunque creo que queria concursar. El alumnado es heterogeneo: hay pikikis (pocos pero la lian en 1 y 2 de eso al principio de curso pero luego dejan de venir). Hay alumnado un poco idiota de comportamiento pero en general son muy bueno, ademas el centro acoge en bachillerato a alumnos de Sabiote que son muy muy buenos. Insisisto: el mejor con diferencia de los que he estado. Tuve alumnos maravillosos y educados.",
     "Estuve alli el curso pasado. Sin duda el mejor centro en el que he estado. Me pude desarrollar como profesional de una manera increible. Claustro poco numeroso (entre 35 y 45), muy buen rollo. Son Comunidad de aprendizaje y se lo curran mogollon. Todos los profes son muy simpaticos y dinamicos: puedes contar con ellos para cualquier cosa. Para mi era el paraiso. El profe de E.F. es mayor pero esta lejos de jubilarse. El alumnado es heterogeneo: hay alumnado que la lia en 1 y 2 de ESO al principio de curso pero luego deja de venir. Hay alumnado un poco idiota de comportamiento pero en general son muy buenos; ademas el centro acoge en bachillerato a alumnos de Sabiote que son muy buenos. Insisto: el mejor con diferencia de los que he estado. Tuve alumnos maravillosos y educados."),
    ("Buen centro. El mejor. Melissa. Hay un interino y un fijo de EF",
     "Buen centro. El mejor. Hay un interino y un fijo de EF."),
    ("Emilio (Amigo Sara): Buen centro. Aunque Directiva horrible se creen que es su cortijo. Companeros muy buenos. Buen ambiente. Alumnado bueno. No definitivos EF, estan de concursillo",
     "Buen centro. Aunque la directiva es horrible, se creen que es su cortijo. Companeros muy buenos. Buen ambiente. Alumnado bueno. No hay definitivos de EF, estan de concursillo."),
    ("Ismael (Almeria): el curso  16-17 habia muy buen rollo: profes jovenes y mayores casi por igual. Habia dos profes de E.F. uno de ellos cercano a la jubilacion. El centro es de compensatoria (los chavales son muy brutos pero nobles) pero se hacen miles de cosas. El ano que yo estuve habia muchos interinos y varios de nosotros viviamos en Orgiva: teniamos nuestro grupo de senderismo y cervezas. Orgiva tiene biblioteca y escuela de idiomas. Alquiler muy barato. Habia mucha gente que iba a veni a Granada. Los pueblos de al lado molan mucho.",
     "El curso 16-17 habia muy buen rollo: profes jovenes y mayores casi por igual. Habia dos profes de E.F., uno de ellos cercano a la jubilacion. El centro es de compensatoria (los chavales son muy brutos pero nobles) pero se hacen miles de cosas. El ano que estuve habia muchos interinos y varios viviamos en Orgiva. Orgiva tiene biblioteca y escuela de idiomas. Alquiler muy barato. Habia mucha gente que se iba a Granada. Los pueblos de al lado molan mucho."),
    ("Novio de Silvia. Buen centro", "Buen centro."),
    ("no1 de Estepona. Insti Maria del Mar Mena. Buen claustro. Buen Dpto EF. Insti tranquilo. En Estepona todos buenos.",
     "El nº1 de Estepona. Buen claustro. Buen departamento de EF. Instituto tranquilo. En Estepona todos buenos."),
    ("Buen centro (esta Maria Calata, aunque es de compensatoria, es equipo docente trabajador e instalaciones muy buenas)",
     "Buen centro (aunque es de compensatoria, es equipo docente trabajador e instalaciones muy buenas)."),
    ("Buen centro. Estuvo hermano Silvia", "Buen centro."),
    ("Mucho extranjero. Mafioso (dicho por Maria Calata)", "Mucho extranjero. Dicen que es mafioso."),
    ("Muy Bueno. Excelente. Estuvo Lourdes Calahorro (Inlges Vilches). MALO Maria del Mar. Compensatoria o Dificil Desempeno. Ciudad desangelada. Muy masificada.",
     "Muy bueno, excelente. Para algunos, malo. Compensatoria o dificil desempeno. Ciudad desangelada. Muy masificada."),
    ("El peor de los 3 de Torremolinos. MALO Maria del Mar. Compensatoria o Dificil Desempeno. Ciudad desangelada. Muy masificada.",
     "El peor de los 3 de Torremolinos. Malo. Compensatoria o dificil desempeno. Ciudad desangelada. Muy masificada."),
    ("MALO Maria del Mar. Compensatoria o Dificil Desempeno. Ciudad desangelada. Muy masificada.",
     "Malo. Compensatoria o dificil desempeno. Ciudad desangelada. Muy masificada."),
    ("Buen centro. Estuvo Ro.", "Buen centro."),
    ("Ismael (Almeria): Tengo una muy buena amiga que ha trabajado este curso alli. Dice que esta super encantada con el alumnado y con los companeros pero que el instituto al ser centro de calidad es una brutalidad la de papeles mierdosos que tienen que estar rellenando practicamente cada semana. El inspector va mucho por alli y la gente se pone muy nerviosa. Mi amiga ha sido tutora y dice que los alumnos muy bien pero que la burocracia ha sido algo salvaje, los acribillan a informes, preevaluaciones, diagnosticos... incluso antes del covid. No repite ni aunque le regalasen la plaza. Hugo creo que trabajo alli.",
     "Cuentan que el alumnado y los companeros son estupendos, pero que el instituto, al ser centro de calidad, tiene una brutalidad de papeleo que hay que rellenar practicamente cada semana. El inspector va mucho por alli y la gente se pone nerviosa. Los alumnos muy bien, pero la burocracia es algo salvaje: acribillan a informes, preevaluaciones, diagnosticos... incluso antes del covid."),
    ("Bueno. Yolanda (hermana Luisa). IESO", "Bueno. Es un IESO."),
    ("Buen centro. Muy grande. // Aqui ha trabajado un muy buen amigo mio y va a repetir el curso que viene. Tiene sus cosas malas como todo ies pero en general el esta contento. El Jefe de estudios es de Clasicas y por lo que me cuenta mi amigo es un hombre conciliador.Buen centro. Muy grande.",
     "Buen centro. Muy grande. Tiene sus cosas malas como todo IES pero en general la gente esta contenta. El jefe de estudios es de Clasicas y es un hombre conciliador."),
    ("Ismael (Almeria): Buen centro. Este es otro de los institutos de solera de Almeria junto con el Celia Vinas. Siempre ha tenido muy buena fama en cuanto a resultados academicos. Esta al lado del conservatorio pero no tengo ni idea de nada mas. Lo siento.",
     "Buen centro. Es otro de los institutos de solera de Almeria, junto con el Celia Vinas. Siempre ha tenido muy buena fama en cuanto a resultados academicos. Esta al lado del conservatorio."),
    ("Ismael (Almeria): Buen centro. Es el instituto donde estudie. Un edificio muy senorial y en pleno centro de Almeria. No tengo n idea de si habra ambiado o no pero sigue siendo un instituto con muy buen fama en Almeria. Inconveniene: el claustro es enorme (mas de 100profes seguro) y la mayoria muy mayores(concursan y acaban jubilandose alli). De todas formas hacen mil millones de actividades. Hay clase en el nocturno y mucha fp. Tiene bachillerato internacional.",
     "Buen centro. Un edificio muy senorial y en pleno centro de Almeria. Sigue siendo un instituto con muy buena fama en Almeria. Inconveniente: el claustro es enorme (mas de 100 profes) y la mayoria muy mayores (concursan y acaban jubilandose alli). De todas formas hacen muchisimas actividades. Hay clase en el nocturno y mucha FP. Tiene bachillerato internacional."),
    ("Regu, mejor que Vilches pero con gitanos. Esta Rosa Porrero",
     "Regular, mejor que Vilches pero con gitanos."),
    ("No tiene mala fama. FP. Centro grande. Al lado del fronton y pistas de tenis con puerta propia de acceso. Al lado del Alcampo (Amparo Mates Vilches, solo sabia esto)",
     "No tiene mala fama. FP. Centro grande. Al lado del fronton y pistas de tenis con puerta propia de acceso. Al lado del Alcampo."),
    ("Buen centro. Estuvo Ro alli", "Buen centro."),
    ("HORRIBLE, Ro estuvo alli", "Horrible."),
    ("Muy bueno. Insti Luisa. IESO", "Muy bueno. Es un IESO."),
]
OVERRIDES = {norm_key(orig): clean for orig, clean in _OVERRIDES_RAW}

# Pasada generica (red de seguridad para atribuciones no contempladas arriba).
_GENERIC_RULES = [
    (re.compile(r"^\s*[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+\s*\([^)]*\)\s*:\s*"), ""),  # "Nombre (Lugar): "
    (re.compile(r"\(\s*dicho por[^)]*\)", re.I), ""),                     # "(dicho por X)"
    (re.compile(r"\bnovi[oa] de\s+\w+\.?", re.I), ""),                    # "novio de X"
    (re.compile(r"\b(herman[oa])\s+\w+\.?", re.I), ""),                   # "hermano X"
]


def sanitize(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    override = OVERRIDES.get(norm_key(text))
    if override is not None:
        return override
    for rx, repl in _GENERIC_RULES:
        text = rx.sub(repl, text)
    return re.sub(r"\s+", " ", text).strip()


def nombres_residuales(text: str) -> list[str]:
    f = f" {_fold(text)} "
    return [n.strip() for n in NOMBRES_VIGILADOS if n.strip() and n in f]


# --------------------------------------------------------------------------
# Carga y cruce
# --------------------------------------------------------------------------

def resolver_columnas(cols: list[str]) -> dict[str, str]:
    """Mapea nombre canonico -> nombre real de columna del Excel."""
    quiero = {
        "codigo": "codigo",
        "nombre": "nombre",
        "municipio": "munic local",
        "info_extra": "info extra ies",
        "info_2024": "info 2024",
    }
    folded = {norm_key(c): c for c in cols}
    out = {}
    for canon, target in quiero.items():
        for fk, real in folded.items():
            if fk.startswith(target):
                out[canon] = real
                break
    return out


def main() -> int:
    try:
        import pandas as pd  # noqa: PLC0415
    except ImportError:
        print("ERROR: falta pandas (pip install pandas openpyxl)", file=sys.stderr)
        return 1

    if not XLSX.exists():
        print(f"ERROR: no existe {XLSX}", file=sys.stderr)
        print("       copia ahi el Excel de opiniones antes de ejecutar.", file=sys.stderr)
        return 1

    centros = json.loads(CENTROS_JSON.read_text(encoding="utf-8"))
    by_cod = {c["codigo"]: c for c in centros}
    idx_nombre: dict[str, list[tuple[str, str]]] = {}      # municipio -> centros
    idx_prov: dict[str, list[tuple[str, str]]] = {}        # provincia -> centros
    for c in centros:
        idx_nombre.setdefault(norm_key(c["municipio"]), []).append(
            (norm_nombre(c["nombre"]), c["codigo"]))
        idx_prov.setdefault(norm_key(c["provincia"]), []).append(
            (norm_nombre(c["nombre"]), c["codigo"]))

    xl = pd.ExcelFile(XLSX)
    acumulado: dict[str, list[str]] = {}      # codigo -> [info saneada, ...]
    revision: list[dict] = []
    sin_match: list[dict] = []
    n_filas = n_info = 0

    for sheet in xl.sheet_names:
        if norm_key(sheet) == "todos":   # hoja resumen, duplica las demas
            continue
        df = pd.read_excel(xl, sheet, header=1)
        df.columns = [str(c).strip() for c in df.columns]
        col = resolver_columnas(list(df.columns))
        if "nombre" not in col:
            continue
        for _, r in df.iterrows():
            nombre = r.get(col["nombre"])
            if not isinstance(nombre, str) or not nombre.strip():
                continue
            n_filas += 1

            partes = []
            for k in ("info_extra", "info_2024"):
                if k in col:
                    v = r.get(col[k])
                    if isinstance(v, str) and v.strip():
                        partes.append(v.strip())
            info_raw = " ".join(partes).strip()
            if not info_raw:
                continue
            n_info += 1

            # --- cruce ---
            cod = norm_codigo(r.get(col["codigo"])) if "codigo" in col else None
            metodo = ""
            if cod and cod in by_cod:
                metodo = "codigo"
            else:
                muni = r.get(col.get("municipio", ""))
                mm = norm_key(muni) if isinstance(muni, str) else ""
                nn = norm_nombre(nombre)
                hits = [c for n, c in idx_nombre.get(mm, []) if n and (n in nn or nn in n)]
                if len(hits) >= 1:
                    cod, metodo = hits[0], ("nombre+municipio" if len(hits) == 1
                                            else "nombre+municipio (ambiguo)")
                else:
                    # 3er fallback: nombre unico dentro de la provincia (hoja).
                    # El municipio del Excel a veces es una localidad (p.ej.
                    # "Torre del Mar") y no casa con el municipio oficial.
                    prov_hits = [c for n, c in idx_prov.get(norm_key(sheet), [])
                                 if n and len(n) > 3 and (n == nn or n in nn or nn in n)]
                    if len(prov_hits) == 1:
                        cod, metodo = prov_hits[0], "nombre+provincia"

            saneada = sanitize(info_raw)
            if not cod or cod not in by_cod:
                sin_match.append({"sheet": sheet, "nombre": nombre.strip(),
                                  "municipio": str(r.get(col.get("municipio", ""))).strip(),
                                  "info": info_raw})
                continue

            acumulado.setdefault(cod, [])
            if saneada and saneada not in acumulado[cod]:
                acumulado[cod].append(saneada)

            residuales = nombres_residuales(saneada)
            if info_raw != saneada or residuales:
                revision.append({
                    "codigo": cod,
                    "centro": by_cod[cod]["nombre"],
                    "metodo": metodo,
                    "nombres_residuales": ", ".join(residuales),
                    "original": info_raw,
                    "saneado": saneada,
                })

    # --- escritura: info_extra_centros.csv ---
    filas = sorted(
        ({"codigo": cod, "info_extra": " ".join(v)} for cod, v in acumulado.items() if v),
        key=lambda x: x["codigo"])
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["codigo", "info_extra"])
        w.writeheader()
        w.writerows(filas)

    # --- escritura: info_extra_revision.csv (auditoria del saneado) ---
    with open(OUT_REVISION, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "codigo", "centro", "metodo", "nombres_residuales", "original", "saneado"])
        w.writeheader()
        w.writerows(sorted(revision, key=lambda x: x["nombres_residuales"], reverse=True))

    # --- resumen ---
    print(f"Filas del Excel con nombre        : {n_filas}")
    print(f"  con texto de opinion            : {n_info}")
    print(f"Centros con info incorporada      : {len(filas)}")
    print(f"Filas saneadas (revisar CSV)      : {len(revision)}")
    pend = [x for x in revision if x["nombres_residuales"]]
    if pend:
        print(f"  AVISO: {len(pend)} con posible nombre residual -> revisa "
              f"'nombres_residuales' en {OUT_REVISION.name}")
    print(f"Filas con info SIN cruzar         : {len(sin_match)}")
    for x in sin_match:
        print(f"    [{x['sheet']}] {x['nombre']}  ({x['municipio']})  ::  {x['info'][:55]}")
    print(f"\nEscrito: {OUT_CSV}")
    print(f"Escrito: {OUT_REVISION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
