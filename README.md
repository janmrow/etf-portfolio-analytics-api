# ETF Portfolio Analytics API

A small **REST API** that evaluates ETF portfolios defined by target weights.

It returns portfolio risk/return metrics and can run a simple historical allocation backtest.
This is a portfolio / learning project focused on:

* **API design and clarity** (OpenAPI-first mindset)
* **Multi-level API testing** (unit, API/integration, contract-style checks)
* **CI automation and quality gates** (lint + tests on every commit)

---

## What it does (non-technical)
You provide a portfolio like “60% SPY, 40% QQQ”.

The API returns key numbers such as **volatility** and **maximum drawdown**, and can simulate how the portfolio value would have evolved historically.

---

## Tech stack (initial)
* **FastAPI**
* **Pytest** + coverage
* **Ruff** (format + lint)
* **GitHub Actions** CI

---

## Local setup

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

## Project structure (initial)
* `app/` — application code (FastAPI app)
* `tests/` — automated tests
* `docs/adr/` — architecture decision records (small and practical)
