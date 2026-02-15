from fastapi import FastAPI

from app.api.v1.routes_etfs import router as v1_etfs_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="ETF Portfolio Analytics API",
        version="0.1.0",
        description=(
            "A small, portfolio-style REST API for ETF analytics and backtesting. "
            "Built as a learning project focused on API quality and test automation."
        ),
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(v1_etfs_router)
    return app


app = create_app()
