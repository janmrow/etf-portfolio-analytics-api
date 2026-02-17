from app.main import create_app
from fastapi.testclient import TestClient


def test_get_prices_defaults_to_full_range() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/prices/VT")

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "VT"
    assert body["count"] == len(body["items"])
    assert body["count"] > 0
    assert body["from"] <= body["to"]


def test_get_prices_filters_by_date_range() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/prices/VT?from=2024-01-05&to=2024-01-10")

    assert response.status_code == 200
    body = response.json()
    assert body["from"] == "2024-01-05"
    assert body["to"] == "2024-01-10"
    assert all("date" in item and "close" in item for item in body["items"])
    assert all("2024-01-05" <= item["date"] <= "2024-01-10" for item in body["items"])


def test_get_prices_unknown_symbol_returns_problem_404() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/prices/NOPE")

    assert response.status_code == 404
    body = response.json()
    assert body["type"] == "not_found"
    assert body["title"] == "Prices not found"
    assert body["instance"] == "/v1/prices/NOPE"


def test_get_prices_from_greater_than_to_returns_422() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/prices/VT?from=2024-01-10&to=2024-01-05")

    assert response.status_code == 422
