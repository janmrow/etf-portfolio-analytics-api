# ETF Portfolio Analytics API

A small **REST API** that evaluates ETF portfolios defined by target weights. It returns portfolio risk/return metrics and can run a simple historical allocation backtest.

This is a portfolio / learning project focused on:
* **API design and clarity** (OpenAPI-first mindset)
* **Multi-level API testing** (unit, API/integration, contract-style checks)
* **CI automation and quality gates** (lint + tests on every commit)

---

## 🧐 What it does

You provide a portfolio like **"60% VT, 40% BND"**.

The API returns key numbers such as **volatility** and **maximum drawdown**, and simulates how the portfolio value would have evolved historically.

---

## 🛠️ Tech stack

* **FastAPI** (Web framework)
* **Pytest** + coverage (Testing)
* **Ruff** (Fastest linter & formatter)
* **GitHub Actions** (CI/CD)

---

## 💻 Local setup

1. **Create and activate a virtualenv:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or venv\Scripts\activate on Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Health check:**
   ```bash
   curl [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
   ```

---

## 🚀 API Endpoints (v1)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/v1/etfs` | Retrieve a list of all available ETFs. |
| `GET` | `/v1/etfs/{symbol}` | Get detailed information for a specific ETF. |
| `GET` | `/v1/prices/{symbol}` | Get historical prices with optional `from` and `to` filters. |

### Examples:
```bash
# List all ETFs
curl [http://127.0.0.1:8000/v1/etfs](http://127.0.0.1:8000/v1/etfs)

# Get specific ETF details
curl [http://127.0.0.1:8000/v1/etfs/VT](http://127.0.0.1:8000/v1/etfs/VT)

# Get prices with date filtering
curl "[http://127.0.0.1:8000/v1/prices/VT?from=2024-01-05&to=2024-01-10](http://127.0.0.1:8000/v1/prices/VT?from=2024-01-05&to=2024-01-10)"
```

---

## ⚙️ Configuration & Quality

### Data Source
By default, the API reads data from `./data`. You can override it via environment variable:
```bash
DATA_DIR=data_alt uvicorn app.main:app --reload
```

### Quality Gates (Run before commit)
```bash
ruff format .   # Auto-format code
ruff check .    # Linting rules
pytest          # Run test suite
```

---

## 🌳 Project structure

The project follows a **modular hexagonal-lite** approach:

* `app/` — Core application logic
    * `api/` — Versioned REST controllers & error handling
    * `domain/` — Pure business logic, entities, and domain exceptions
    * `infra/` — Data persistence (JSON store & Repositories)
    * `main.py` — Entry point and router wiring
* `data/` — Local storage for market data (`etfs.json`, `prices/*.json`)
* `docs/adr/` — **Architecture Decision Records** (e.g., error strategy)
* `tests/` — Automated test suite (Integration & Unit)
* `.github/` — CI workflows (Ruff, Pytest)
