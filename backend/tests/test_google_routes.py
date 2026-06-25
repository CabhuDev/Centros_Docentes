def test_geocode(client, mock_google):
    r = client.post("/api/geocode", json={"address": "Gran Via, Granada"})
    assert r.status_code == 200
    body = r.json()
    assert body["lat"] == 37.18
    assert "mock" in body["formatted_address"]


def test_distancias(client, mock_google):
    # Tomamos codigos reales de un filtro
    centros = client.get("/api/centros", params={"provincia": "Granada", "limit": 3}).json()
    codigos = [c["codigo"] for c in centros["items"]]
    r = client.post("/api/distancias", json={
        "origin": {"lat": 37.18, "lng": -3.60},
        "codigos": codigos,
        "mode": "driving",
    })
    assert r.status_code == 200
    res = r.json()["results"]
    assert len(res) == len(codigos)
    assert all(x["status"] == "OK" for x in res)
    assert res[0]["duration_text"] == "1 min"


def test_distancias_codigo_invalido(client, mock_google):
    r = client.post("/api/distancias", json={
        "origin": {"lat": 37.18, "lng": -3.60},
        "codigos": ["00000000"],
        "mode": "driving",
    })
    assert r.status_code == 400
