"""Carga en memoria de los centros y el catalogo de filtros."""
from __future__ import annotations

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


class DataStore:
    def __init__(self) -> None:
        self.centros: list[dict] = []
        self.meta: dict = {}
        self.by_codigo: dict[str, dict] = {}
        # Filas originales completas (todas las columnas del CSV de origen).
        self.raw_columns: list[str] = []
        self.raw_by_codigo: dict[str, dict] = {}
        self.load()

    def load(self) -> None:
        with open(DATA_DIR / "centros.json", encoding="utf-8") as f:
            self.centros = json.load(f)
        with open(DATA_DIR / "meta.json", encoding="utf-8") as f:
            self.meta = json.load(f)
        with open(DATA_DIR / "centros_raw.json", encoding="utf-8") as f:
            raw = json.load(f)
        self.raw_columns = raw["columns"]
        self.raw_by_codigo = raw["by_codigo"]
        self.by_codigo = {c["codigo"]: c for c in self.centros}


store = DataStore()
