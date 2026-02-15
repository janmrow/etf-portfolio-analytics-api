# ADR 0001: Tooling and Code Style

## Status
**Accepted**

---

## Context
This project is a learning playground for building and testing a small REST API.

The primary goal is **clarity and testability**, not maximum cleverness or minimal code.
We want:
* Simple, readable Python code.
* Fast feedback loops (lint + tests on every commit via CI).
* A clean baseline to incrementally add endpoints and tests.

---

## Decision
* **Language:** Python 3.11+
* **Web framework:** FastAPI (built-in OpenAPI, strong request/response models)
* **Formatting + linting:** Ruff (single tool for both)
* **Testing:** Pytest (+ coverage)
* **CI:** GitHub Actions running format check, lint, and tests.

---

## Consequences
* Contributors follow the same formatting/lint rules locally and in CI.
* The repository starts with a green pipeline and grows commit-by-commit.
* We prioritize explicit code and clear naming over clever abstractions.
