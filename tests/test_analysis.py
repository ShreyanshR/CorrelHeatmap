from __future__ import annotations

from datetime import date, timedelta

import pytest

from correlheatmap.analysis import CorrelationResult, compute_correlation_matrix, compute_returns
from correlheatmap.data import PriceHistory


def make_price_series(start: date, prices: list[float]) -> list[tuple[date, float]]:
    return [(start + timedelta(days=i), price) for i, price in enumerate(prices)]


def test_compute_returns_log() -> None:
    series = make_price_series(date(2024, 1, 1), [100.0, 110.0, 121.0])
    returns = compute_returns(series, return_type="log")
    assert len(returns) == 2
    assert pytest.approx(returns[0][1], rel=1e-9) == 0.0953101798
    assert pytest.approx(returns[1][1], rel=1e-9) == 0.0953101798


def test_compute_returns_pct() -> None:
    series = make_price_series(date(2024, 1, 1), [50.0, 55.0, 60.5])
    returns = compute_returns(series, return_type="pct")
    assert [round(value, 4) for _, value in returns] == [0.1, 0.1]


def test_compute_correlation_matrix_basic() -> None:
    history: PriceHistory = {
        "AAA": make_price_series(date(2024, 1, 1), [100, 102, 104, 103, 105]),
        "BBB": make_price_series(date(2024, 1, 1), [50, 51, 52, 51, 53]),
        "CCC": make_price_series(date(2024, 1, 1), [200, 198, 202, 205, 207]),
    }
    result = compute_correlation_matrix(history, return_type="pct")
    assert isinstance(result, CorrelationResult)
    assert result.tickers == ["AAA", "BBB", "CCC"]
    assert result.observation_count == 4
    assert result.matrix[0][0] == pytest.approx(1.0)
    assert result.matrix[1][1] == pytest.approx(1.0)
    assert result.matrix[2][2] == pytest.approx(1.0)
    assert -1.0 <= result.matrix[0][1] <= 1.0


def test_compute_correlation_requires_two_tickers() -> None:
    history: PriceHistory = {"AAA": make_price_series(date(2024, 1, 1), [100, 101, 102])}
    with pytest.raises(ValueError):
        compute_correlation_matrix(history)


def test_compute_returns_requires_positive_prices() -> None:
    series = make_price_series(date(2024, 1, 1), [100.0, 0.0, 120.0])
    with pytest.raises(ValueError):
        compute_returns(series)
