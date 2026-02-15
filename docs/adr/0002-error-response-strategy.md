# ADR 0002: Error Response Strategy

## Status
**Accepted**

---

## Context
As soon as we introduced real domain behavior (e.g. unknown ETF symbol), we needed predictable error responses.

* **Default framework validation errors (422)** are fine for now.
* **Domain-level errors** (like "not found") should be stable and easy to assert in tests.

---

## Decision
For domain-level errors (e.g. resource not found), return a small **"problem-style"** JSON object containing:
* `type`
* `title`
* `status`
* `detail`
* `instance`

> **Note:** For request validation errors (422), we will keep FastAPI defaults in early iterations. We will unify 422 responses later once the API surface grows.

---

## Consequences
* **Consistency:** Tests can assert error shape consistently for 404 cases.
* **Developer Experience:** Clients get a stable, readable error payload.
* **Agility:** We avoid premature complexity while keeping a clear migration path to full unification.
