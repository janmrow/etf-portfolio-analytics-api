from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    Application factory to keep the app setup explicit and test-friendly.
    """
    app = FastAPI(
        title="ETF Portfolio Analytics API",
        version="0.1.0",
        description=(
            "A small, portfolio-style REST API for ETF analytics and backtesting. "
            "Built as a learning project focused on API quality and test automation."
        ),
    )
    return app


app = create_app()
