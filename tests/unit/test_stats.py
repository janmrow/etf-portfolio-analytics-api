import math

import pytest
from app.domain.stats import compute_stats, daily_returns, max_drawdown, volatility_annualized


def test_daily_returns_empty_when_not_enough_prices() -> None:
    assert daily_returns([]) == []
    assert daily_returns([100.0]) == []


def test_daily_returns_computes_simple_returns() -> None:
    prices = [100.0, 110.0, 99.0]
    # 110/100 - 1 = 0.10
    # 99/110 - 1 = -0.10
    rets = daily_returns(prices)
    assert rets == pytest.approx([0.10, -0.10], abs=1e-12)


def test_daily_returns_rejects_non_positive_prices() -> None:
    with pytest.raises(ValueError):
        daily_returns([100.0, 0.0])


def test_max_drawdown_zero_when_not_enough_prices() -> None:
    assert max_drawdown([]) == 0.0
    assert max_drawdown([100.0]) == 0.0


def test_max_drawdown_simple_case() -> None:
    # Peak at 120, trough at 90 => dd = (120-90)/120 = 0.25
    prices = [100.0, 120.0, 90.0, 110.0]
    assert max_drawdown(prices) == pytest.approx(0.25, abs=1e-12)


def test_max_drawdown_monotonic_increase_is_zero() -> None:
    prices = [100.0, 101.0, 102.0, 110.0]
    assert max_drawdown(prices) == pytest.approx(0.0, abs=1e-12)


def test_volatility_annualized_returns_zero_for_small_samples() -> None:
    assert volatility_annualized([]) == 0.0
    assert volatility_annualized([0.01]) == 0.0


def test_volatility_annualized_matches_known_sample() -> None:
    # Simple symmetric returns around mean 0: [0.01, -0.01]
    # Sample variance = ((0.01^2 + 0.01^2) / (2-1)) = 0.0002
    # Daily stdev = sqrt(0.0002)
    # Annualized = daily_stdev * sqrt(252)
    rets = [0.01, -0.01]
    expected = math.sqrt(0.0002) * math.sqrt(252)
    assert volatility_annualized(rets) == pytest.approx(expected, rel=1e-12)


def test_compute_stats_smoke() -> None:
    prices = [100.0, 101.0, 99.0, 102.0]
    result = compute_stats(prices)
    assert result.max_drawdown >= 0.0
    assert result.volatility_annualized >= 0.0
