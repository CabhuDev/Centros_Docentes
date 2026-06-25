"""
Preprocesa el CSV oficial del Directorio de Centros Docentes de Andalucia
(curso 2024/2025) y genera dos ficheros JSON limpios para el backend:

  backend/app/data/centros.json  -> lista de centros normalizados
  backend/app/data/meta.json     -> catalogo para los filtros del frontend

Uso:
  python scripts/preprocess.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "datos" / "centros_24-25.csv"
# Capa opcional de opiniones/experiencias de profesorado (ver
# scripts/build_info_extra.py). Si no existe, se omite sin error.
INFO_EXTRA_SRC = ROOT / "datos" / "info_extra_centros.csv"
OUT_DIR = ROOT / "backend" / "app" / "data"

# --------------------------------------------------------------------------
# Catalogo de etapas y enseñanzas concretas.
# Cada etapa (nivel grueso) agrupa varias "ensenanzas" (modalidad concreta:
# ordinario / adultos / semipresencial / regladas / no regladas...). Cada
# ensenanza agrupa las columnas S/N del CSV (variantes pub/priv de la misma
# modalidad). Un centro "imparte" la ensenanza si CUALQUIER columna vale "S",
# y la etapa si imparte CUALQUIER ensenanza suya.
#
# Estructura: (etapa_key, etapa_label, [ (ens_key, ens_label, [columnas]) ... ])
# --------------------------------------------------------------------------
ETAPAS = [
    ("infantil_1ciclo", "Infantil 1.er ciclo (0-3)", [
        ("inf1", "Primer ciclo (0-3 años)",
            ["pub_adh_inf1", "pub_noadh_inf1", "priv_adh_inf1", "priv_noadh_inf1"]),
    ]),
    ("infantil_2ciclo", "Infantil 2.o ciclo (3-6)", [
        ("inf2", "Segundo ciclo (3-6 años)",
            ["pub_inf2", "priv_c_inf2", "priv_noc_inf2"]),
    ]),
    ("primaria", "Educación Primaria", [
        ("pri", "Educación Primaria", ["pub_pri", "priv_c_pri", "priv_noc_pri"]),
    ]),
    ("eso", "ESO", [
        ("eso", "Educación Secundaria Obligatoria",
            ["pub_eso", "priv_c_eso", "priv_noc_eso"]),
    ]),
    ("bachillerato", "Bachillerato", [
        ("bach_ord", "Bachillerato ordinario",
            ["pub_bach_ord", "priv_c_bach_ord", "priv_noc_bach_ord"]),
        ("bach_adul", "Bachillerato para personas adultas", ["pub_bach_adul"]),
        ("bach_dist", "Bachillerato semipresencial / distancia", ["pub_bach_semi_dist"]),
    ]),
    ("fp_basica", "FP Básica", [
        ("fpbas", "Ciclos Formativos de Grado Básico",
            ["pub_fpbasica", "priv_c_fpbas", "priv_noc_fpbas"]),
    ]),
    ("fp_grado_medio", "FP Grado Medio", [
        ("fpgm_ord", "FP Grado Medio ordinario",
            ["pub_fpgm_ord", "priv_c_fpgm_ord", "priv_noc_fpgm_ord"]),
        ("fpgm_adul", "FP Grado Medio para adultos", ["pub_fpgm_adul"]),
        ("fpgm_dist", "FP Grado Medio semipresencial / distancia",
            ["pub_fpgm_semi_dist", "priv_noc_fpgm_semi_dist"]),
    ]),
    ("fp_grado_superior", "FP Grado Superior", [
        ("fpgs_ord", "FP Grado Superior ordinario",
            ["pub_fpgs_ord", "priv_c_fpgs_ord", "priv_noc_fpgs_ord"]),
        ("fpgs_adul", "FP Grado Superior para adultos",
            ["pub_fpgs_adul", "priv_noc_fpgs_adul"]),
        ("fpgs_dist", "FP Grado Superior semipresencial / distancia",
            ["pub_fpgs_semi_dist", "priv_noc_fpgs_semi_dist"]),
    ]),
    ("fp_especializacion", "Cursos de Especialización FP", [
        ("ce_gm", "Especialización de Grado Medio", ["pub_ce_gm", "pri_noc_ce_gm"]),
        ("ce_gs", "Especialización de Grado Superior", ["pub_ce_gs", "pri_noc_ce_gs"]),
    ]),
    ("educacion_especial", "Educación Especial", [
        ("ee", "Educación Especial", ["pub_ee", "priv_c_ee", "priv_noc_ee"]),
    ]),
    ("artes_plasticas_diseno", "Artes Plásticas y Diseño", [
        ("apd_gm", "APD - Grado Medio", ["pub_ccff_gm_apd", "priv_ccff_gm_apd"]),
        ("apd_gs", "APD - Grado Superior", ["pub_ccff_gs_apd", "priv_ccff_gs_apd"]),
    ]),
    ("ensenanzas_superiores", "Enseñanzas Artísticas Superiores", [
        ("escr", "Conservación y Restauración de Bienes Culturales",
            ["pub_ESCR", "priv_ESCR"]),
        ("esd", "Estudios Superiores de Diseño", ["pub_ESD", "priv_ESD"]),
        ("master_ea", "Máster de Enseñanzas Artísticas", ["priv_Master_EA"]),
    ]),
    ("arte_dramatico", "Arte Dramático", [
        ("dra", "Arte Dramático", ["pub_Dra", "priv_Dra"]),
    ]),
    ("musica", "Música", [
        ("mus_reg", "Música (regladas)", ["pub_Ens_Mus", "priv_Ens_Mus"]),
        ("mus_noreg", "Música (no regladas)",
            ["pub_Ens_no_reg_mus", "priv_Ens_no_reg_mus"]),
    ]),
    ("danza", "Danza", [
        ("dan_reg", "Danza (regladas)", ["pub_Ens_Dan", "priv_Ens_Dan"]),
        ("dan_noreg", "Danza (no regladas)",
            ["pub_Ens_no_reg_dan", "priv_Ens_no_reg_dan"]),
    ]),
    ("idiomas", "Idiomas (EOI)", [
        ("eoi", "Escuela Oficial de Idiomas", ["pub_idi", "pub_idi_libre"]),
        ("idi_noreg", "Idiomas (no regladas)", ["pub_Ens_no_reg_idi"]),
    ]),
    ("deportivas", "Enseñanzas Deportivas", [
        ("dep_gm", "Deportivas de Grado Medio", ["pub_Dep_gm", "priv_Dep_gm"]),
        ("dep_gs", "Deportivas de Grado Superior", ["pub_Dep_gs", "priv_Dep_gs"]),
    ]),
    ("adultos", "Educación de Adultos", [
        ("adul_formal", "Educación de adultos formal", ["pub_Adul_formal"]),
        ("adul_noformal", "Educación de adultos no formal (planes)", ["pub_planes"]),
    ]),
]


def read_rows(path: Path):
    """Lee el CSV probando UTF-8 y con respaldo latin-1."""
    for enc in ("utf-8", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                rows = list(csv.DictReader(f, delimiter=";"))
            print(f"  leido con encoding={enc}")
            return rows
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"No se pudo decodificar {path}")


def to_float(val: str):
    """Convierte coordenada con coma decimal a float; None si invalida."""
    if not val:
        return None
    try:
        return float(val.strip().replace(",", "."))
    except ValueError:
        return None


def clean(val: str):
    return (val or "").strip()


def load_info_extra(path: Path) -> dict[str, str]:
    """Lee codigo,info_extra (UTF-8). Devuelve {} si el fichero no existe."""
    if not path.exists():
        print(f"  (sin capa info_extra: no existe {path.name})")
        return {}
    with open(path, encoding="utf-8") as f:
        info = {clean(r.get("codigo")): clean(r.get("info_extra"))
                for r in csv.DictReader(f)}
    info = {k: v for k, v in info.items() if k and v}
    print(f"  info_extra: {len(info)} centros con opiniones")
    return info


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: no existe {SRC}", file=sys.stderr)
        return 1

    print(f"Leyendo {SRC.name} ...")
    rows = read_rows(SRC)
    header = list(rows[0].keys()) if rows else []
    info_extra = load_info_extra(INFO_EXTRA_SRC)

    # Validar que las columnas del catalogo existen en el CSV real
    known = set(header)
    missing = []
    for _ekey, _elabel, ensenanzas in ETAPAS:
        for _key, _label, cols in ensenanzas:
            for c in cols:
                if c not in known:
                    missing.append(c)
    if missing:
        print("AVISO: columnas del catalogo no encontradas en el CSV:", missing)

    centros = []
    sin_coords = 0
    for row in rows:
        lat = to_float(row.get("N_LATITUD"))
        lng = to_float(row.get("N_LONGITUD"))
        if lat is None or lng is None:
            sin_coords += 1

        etapas = []
        ensenanzas = []
        for ekey, _elabel, ens_list in ETAPAS:
            imparte_etapa = False
            for key, _label, cols in ens_list:
                if any(clean(row.get(c)).upper() == "S" for c in cols):
                    ensenanzas.append(key)
                    imparte_etapa = True
            if imparte_etapa:
                etapas.append(ekey)

        concertado = any(
            clean(row.get(c)).upper() == "S"
            for c in known if c.startswith("priv_c_")
        )

        codigo = clean(row.get("codigo"))
        centros.append({
            "codigo": codigo,
            "denominacion": clean(row.get("D_DENOMINA")),
            "nombre": clean(row.get("D_ESPECIFICA")),
            "titularidad": clean(row.get("D_TIPO")),
            "concertado": concertado,
            "domicilio": clean(row.get("D_DOMICILIO")),
            "localidad": clean(row.get("D_LOCALIDAD")),
            "cod_municipio": clean(row.get("cod_municipio")),
            "municipio": clean(row.get("D_MUNICIPIO")),
            "provincia": clean(row.get("D_PROVINCIA")),
            "cp": clean(row.get("C_POSTAL")),
            "telefono": clean(row.get("N_TELEFONO")),
            "email": clean(row.get("Correo_e")),
            "lat": lat,
            "lng": lng,
            "regimen_general": clean(row.get("Regimen_general")).upper() == "S",
            "regimen_adultos": clean(row.get("Regimen_adultos")).upper() == "S",
            "regimen_especial": clean(row.get("Regimen_especial")).upper() == "S",
            "etapas": etapas,
            "ensenanzas": ensenanzas,
            # Opiniones/experiencias de profesorado (no verificadas). "" si no hay.
            "info_extra": info_extra.get(codigo, ""),
        })

    # ---- meta.json: catalogo para los filtros ----
    provincias = sorted({c["provincia"] for c in centros if c["provincia"]})
    municipios_por_provincia = {}
    for c in centros:
        if c["provincia"] and c["municipio"]:
            municipios_por_provincia.setdefault(c["provincia"], set()).add(c["municipio"])
    municipios_por_provincia = {
        p: sorted(m) for p, m in sorted(municipios_por_provincia.items())
    }
    denominaciones = sorted({c["denominacion"] for c in centros if c["denominacion"]})

    meta = {
        "curso": "2024/2025",
        "fuente": "Junta de Andalucia - Directorio de Centros Docentes (CC BY 4.0)",
        "total_centros": len(centros),
        "provincias": provincias,
        "municipios_por_provincia": municipios_por_provincia,
        "denominaciones": denominaciones,
        "titularidades": sorted({c["titularidad"] for c in centros if c["titularidad"]}),
        "etapas": [
            {
                "key": ekey,
                "label": elabel,
                "ensenanzas": [{"key": k, "label": lbl} for k, lbl, _ in ens_list],
            }
            for ekey, elabel, ens_list in ETAPAS
        ],
    }

    # ---- centros_raw.json: filas originales completas (para exportar a CSV
    # todos los campos de origen, sin perder ninguna columna) ----
    raw = {
        "columns": header,
        "by_codigo": {clean(row.get("codigo")): row for row in rows},
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "centros.json").write_text(
        json.dumps(centros, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "centros_raw.json").write_text(
        json.dumps(raw, ensure_ascii=False), encoding="utf-8")

    print(f"OK -> {len(centros)} centros")
    print(f"   sin coordenadas validas: {sin_coords}")
    print(f"   provincias: {len(provincias)} | municipios: "
          f"{sum(len(v) for v in municipios_por_provincia.values())}")
    print(f"   escrito: {OUT_DIR / 'centros.json'}")
    print(f"   escrito: {OUT_DIR / 'meta.json'}")
    print(f"   escrito: {OUT_DIR / 'centros_raw.json'} ({len(header)} columnas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
