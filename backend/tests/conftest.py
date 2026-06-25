import pytest
from fastapi.testclient import TestClient

from app import google
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_google(monkeypatch):
    """Sustituye las llamadas reales a Google por respuestas deterministas,
    para que los tests no usen red ni cuota."""

    async def fake_geocode(address):
        return {"lat": 37.18, "lng": -3.60, "formatted_address": f"{address} (mock)"}

    async def fake_distance_matrix(origin, destinos, mode="driving"):
        out = []
        for i, d in enumerate(destinos):
            out.append({
                "codigo": d["codigo"],
                "status": "OK",
                "distance_m": 1000 * (i + 1),
                "distance_text": f"{i + 1} km",
                "duration_s": 60 * (i + 1),
                "duration_text": f"{i + 1} min",
            })
        return out

    monkeypatch.setattr(google, "geocode", fake_geocode)
    monkeypatch.setattr(google, "distance_matrix", fake_distance_matrix)
