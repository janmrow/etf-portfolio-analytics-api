# ETF Portfolio Analytics API

A small **REST API** that evaluates ETF portfolios defined by target weights.

It returns portfolio risk/return metrics and can run a simple historical allocation backtest.
This is a portfolio / learning project focused on:

* **API design and clarity** (OpenAPI-first mindset)
* **Multi-level API testing** (unit, API/integration, contract-style checks)
* **CI automation and quality gates** (lint + tests on every commit)

---

## 🧐 What it does

You provide a portfolio like “60% SPY, 40% QQQ”.

The API returns key numbers such as **volatility** and **maximum drawdown**, and can simulate how the portfolio value would have evolved historically.

---

## 🛠️ Tech stack

* **FastAPI**
* **Pytest** + coverage
* **Ruff** (format + lint)
* **GitHub Actions** CI

---

## 💻 Local setup

1. **Create a virtualenv and install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run tests:**
   ```bash
   pytest
   ```

3. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Health check:**
   ```bash
   curl http://127.0.0.1:8000/health
   ```

---

## 🚀 API Endpoints (v1)

The following endpoints are available in the current version of the API:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/v1/etfs` | Retrieve a list of all available ETFs. |
| `GET` | `/v1/etfs/{symbol}` | Get detailed information for a specific ETF by its symbol. |

---

## 🌳 Project structure

The project follows a modular hexagonal-lite approach, separating business rules from technical implementation:

* `app/` — Core application logic (FastAPI)
    * `api/` — Versioned REST controllers and "Problem-style" error handling
    * `domain/` — Pure business logic, entities, and custom domain exceptions
    * `infra/` — Data persistence implementation (JSON store & Repositories)
    * `main.py` — Application entry point and router wiring
* `data/` — Local storage for static market data (`etfs.json`)
* `docs/adr/` — **Architecture Decision Records** (tracking key technical choices like error strategy)
* `tests/` — Automated test suite
    * `api/` — Integration tests (FastAPI `TestClient`)
    * `unit/` — Lower-level logic tests (e.g., `JsonStore` edge cases)
* `.github/` — CI/CD workflows for automated linting (Ruff) and testing (Pytest)
