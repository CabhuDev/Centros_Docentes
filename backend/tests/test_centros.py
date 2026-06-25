def test_filtro_provincia(client):
    r = client.get("/api/centros", params={"provincia": "Granada", "limit": 5}).json()
    assert r["total"] > 0
    assert all(c["provincia"] == "Granada" for c in r["items"])


def test_titularidad_insensible_a_acentos(client):
    con = client.get("/api/centros", params={"titularidad": "Público"}).json()["total"]
    sin = client.get("/api/centros", params={"titularidad": "publico"}).json()["total"]
    assert con == sin > 0


def test_filtro_ensenanza_concreta(client):
    r = client.get("/api/centros", params={"ensenanzas": "bach_adul"}).json()
    assert r["total"] > 0
    assert all("bach_adul" in c["ensenanzas"] for c in r["items"])


def test_ensenanzas_match_all_es_mas_restrictivo(client):
    params_any = [("ensenanzas", "fpgm_ord"), ("ensenanzas", "fpgs_ord"), ("ensenanzas_match", "any")]
    params_all = [("ensenanzas", "fpgm_ord"), ("ensenanzas", "fpgs_ord"), ("ensenanzas_match", "all")]
    total_any = client.get("/api/centros", params=params_any).json()["total"]
    total_all = client.get("/api/centros", params=params_all).json()["total"]
    assert total_all <= total_any


def test_orden_por_cercania(client):
    # Centro de Granada: el primer resultado debe estar mas cerca que el ultimo
    r = client.get("/api/centros", params={
        "provincia": "Granada", "lat": 37.1773, "lng": -3.5986, "limit": 50,
    }).json()
    dists = [c["distancia_recta_km"] for c in r["items"]]
    assert dists == sorted(dists)
    assert dists[0] < 5


def test_sin_origen_no_hay_distancia(client):
    r = client.get("/api/centros", params={"provincia": "Granada", "limit": 3}).json()
    assert "distancia_recta_km" not in r["items"][0]
