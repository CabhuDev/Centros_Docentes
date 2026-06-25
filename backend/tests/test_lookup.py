def test_lookup_basico(client):
    r = client.post("/api/lookup", json={"codigos": ["04000018", "18002991"]})
    assert r.status_code == 200
    d = r.json()
    assert d["total"] == 2
    assert d["encontrados"] == 2
    assert all(it["encontrado"] for it in d["items"])
    assert d["items"][0]["nombre"]


def test_lookup_cero_inicial_y_no_encontrado(client):
    r = client.post("/api/lookup", json={"codigos": ["4000018", "99999999"]})
    d = r.json()
    # "4000018" se resuelve a "04000018"
    assert d["items"][0]["encontrado"] is True
    assert d["items"][0]["codigo"] == "04000018"
    # inexistente
    assert d["items"][1]["encontrado"] is False
    assert d["encontrados"] == 1


def test_lookup_conserva_orden(client):
    cods = ["18002991", "04000018"]
    r = client.post("/api/lookup", json={"codigos": cods})
    d = r.json()
    assert [it["codigo"] for it in d["items"]] == cods
