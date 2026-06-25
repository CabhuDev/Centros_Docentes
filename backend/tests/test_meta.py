def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["total_centros"] > 7000


def test_meta_estructura(client):
    m = client.get("/api/meta").json()
    assert m["curso"] == "2024/2025"
    assert "Granada" in m["provincias"]
    assert len(m["provincias"]) == 8
    # cada etapa trae sus ensenanzas anidadas
    etapas = {e["key"]: e for e in m["etapas"]}
    assert "bachillerato" in etapas
    sub = {s["key"] for s in etapas["bachillerato"]["ensenanzas"]}
    assert {"bach_ord", "bach_adul", "bach_dist"} <= sub


def test_municipios_por_provincia(client):
    m = client.get("/api/meta").json()
    assert "Granada" in m["municipios_por_provincia"]
    assert "Granada" in m["municipios_por_provincia"]["Granada"]
