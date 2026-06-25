def test_export_csv_orden_y_campos(client):
    body = {
        "items": [
            {"codigo": "18002991", "duration_text": "6 min", "distance_text": "1,2 km", "distancia_recta_km": 0.9},
            {"codigo": "04000018", "duration_text": "45 min", "distance_text": "40 km", "distancia_recta_km": 30.1},
        ],
        "mode": "driving",
    }
    r = client.post("/api/export", json=body)
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    assert "attachment" in r.headers["content-disposition"]
    # BOM para Excel
    assert r.content[:3] == b"\xef\xbb\xbf"

    lines = r.content.decode("utf-8-sig").splitlines()
    header = lines[0].split(";")
    # orden_preferencia + 4 de viaje + 89 originales
    assert header[0] == "orden_preferencia"
    assert "curso" in header and "codigo" in header
    assert len(header) == 94
    # orden respetado
    assert lines[1].split(";")[0] == "1"
    assert lines[2].split(";")[0] == "2"
    assert lines[1].split(";")[6] == "18002991"  # columna codigo


def test_export_sin_datos_viaje_omite_columnas(client):
    body = {"items": [{"codigo": "18002991"}]}
    r = client.post("/api/export", json=body)
    assert r.status_code == 200
    header = r.content.decode("utf-8-sig").splitlines()[0].split(";")
    assert "modo_transporte" not in header
    assert header == ["orden_preferencia"] + _columns(client)


def test_export_codigo_invalido(client):
    r = client.post("/api/export", json={"items": [{"codigo": "00000000"}]})
    assert r.status_code == 400


def _columns(client):
    # columnas originales segun el backend
    from app.data_store import store
    return store.raw_columns
