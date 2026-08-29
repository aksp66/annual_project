import base64

import pytest
from fastapi.testclient import TestClient

from app.api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health_endpoint_reports_loaded_models(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "ddpm_model" in body["models_loaded"] or "gan_generator" in body["models_loaded"]


def test_generate_gan_returns_valid_base64_image(client):
    response = client.get("/generate", params={"model": "gan", "n": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "gan"
    assert body["n"] == 2
    assert len(body["images"]) == 2
    decoded = base64.b64decode(body["images"][0])
    assert decoded[:8] == b"\x89PNG\r\n\x1a\n"  # signature PNG


def test_generate_invalid_model_param_returns_422(client):
    response = client.get("/generate", params={"model": "not_a_model"})
    assert response.status_code == 422


def test_generate_gan_n_too_large_returns_400(client):
    response = client.get("/generate", params={"model": "gan", "n": 9999})
    assert response.status_code == 400


def test_generate_ddpm_n_too_large_returns_400(client):
    response = client.get("/generate", params={"model": "ddpm", "n": 9999})
    assert response.status_code == 400


def test_generate_ddpm_returns_valid_base64_image(client):
    response = client.get("/generate", params={"model": "ddpm", "n": 1})
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "ddpm"
    decoded = base64.b64decode(body["images"][0])
    assert decoded[:8] == b"\x89PNG\r\n\x1a\n"
