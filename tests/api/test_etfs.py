from app.main import create_app
from fastapi.testclient import TestClient


def test_list_etfs_returns_items_and_count() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/etfs")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert body["count"] == len(body["items"])
    assert body["count"] >= 5


def test_get_etf_returns_details() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/etfs/SPY")

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "SPY"
    assert body["currency"] == "USD"
    assert "name" in body


def test_get_etf_unknown_symbol_returns_problem_404() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/etfs/NOPE")

    assert response.status_code == 404
    body = response.json()
    assert body["type"] == "not_found"
    assert body["status"] == 404
    assert body["title"] == "ETF not found"
    assert "Unknown symbol" in body["detail"]
    assert body["instance"] == "/v1/etfs/NOPE"
