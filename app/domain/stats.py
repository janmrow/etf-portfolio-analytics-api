from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class StatsResult:
    volatility_annualized: float
    max_drawdown: float


def daily_returns(prices: list[float]) -> list[float]:
    """
    Compute simple daily returns from a list of prices.
    returns[i] corresponds to return between prices[i] and prices[i+1].

    Requirements:
    - prices must have at least 2 points
    - prices must be positive
    """
    if len(prices) < 2:
        return []

    for p in prices:
        if p <= 0:
            raise ValueError("prices must be positive")

    returns: list[float] = []
    for prev, curr in zip(prices, prices[1:], strict=False):
        returns.append((curr / prev) - 1.0)
    return returns


def volatility_annualized(returns: list[float], trading_days: int = 252) -> float:
    """
    Annualized volatility using sample standard deviation of daily returns.

    - If fewer than 2 return observations, volatility is 0.0
    - Uses sample stdev (n-1) because it's the common convention in finance.
    """
    if len(returns) < 2:
        return 0.0

    mean = sum(returns) / len(returns)
    var = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    return math.sqrt(var) * math.sqrt(trading_days)


def max_drawdown(prices: list[float]) -> float:
    """
    Max drawdown computed from price series.

    Returns a value in [0, 1], e.g. 0.20 means -20% peak-to-trough decline.
    If prices is empty or has one point, drawdown is 0.0.
    """
    if len(prices) < 2:
        return 0.0

    for p in prices:
        if p <= 0:
            raise ValueError("prices must be positive")

    peak = prices[0]
    max_dd = 0.0

    for p in prices:
        if p > peak:
            peak = p
        dd = (peak - p) / peak
        if dd > max_dd:
            max_dd = dd

    return max_dd


def compute_stats(prices: list[float], trading_days: int = 252) -> StatsResult:
    """
    Convenience helper to compute the two key metrics we care about in MVP.
    """
    rets = daily_returns(prices)
    vol = volatility_annualized(rets, trading_days=trading_days)
    dd = max_drawdown(prices)
    return StatsResult(volatility_annualized=vol, max_drawdown=dd)
