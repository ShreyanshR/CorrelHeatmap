"""Pure-Python correlation calculations for price history data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import isclose, log, sqrt
from statistics import mean
from typing import Dict, List, Sequence, Tuple

from .data import PriceHistory, PricePoint

ReturnPoint = Tuple[date, float]


@dataclass
class CorrelationResult:
    tickers: List[str]
    matrix: List[List[float]]
    observation_count: int


def compute_returns(series: Sequence[PricePoint], *, return_type: str = "log") -> List[ReturnPoint]:
    """Compute daily returns from a time-ordered price series."""

    if len(series) < 2:
        raise ValueError("At least two price observations are required to compute returns.")

    if return_type not in {"log", "pct"}:
        raise ValueError("Return type must be 'log' or 'pct'.")

    ordered = sorted(series, key=lambda item: item[0])
    returns: List[ReturnPoint] = []

    previous_date, previous_price = ordered[0]
    for current_date, current_price in ordered[1:]:
        if previous_price <= 0 or current_price <= 0:
            previous_date, previous_price = current_date, current_price
            continue
        if return_type == "log":
            value = log(current_price / previous_price)
        else:
            value = (current_price - previous_price) / previous_price
        returns.append((current_date, value))
        previous_date, previous_price = current_date, current_price

    if not returns:
        raise ValueError("Unable to compute returns due to non-positive prices or insufficient data.")
    return returns


def _align_returns(
    price_history: PriceHistory, *, return_type: str = "log"
) -> Tuple[List[str], List[List[float]]]:
    ticker_returns: Dict[str, Dict[date, float]] = {}
    for ticker, series in price_history.items():
        returns = compute_returns(series, return_type=return_type)
        ticker_returns[ticker] = {obs_date: value for obs_date, value in returns}

    tickers = sorted(ticker_returns.keys())
    if len(tickers) < 2:
        raise ValueError("At least two tickers are required to compute correlations.")

    common_dates = set.intersection(*(set(values.keys()) for values in ticker_returns.values()))
    if len(common_dates) < 2:
        raise ValueError("Not enough overlapping return observations across tickers.")

    sorted_dates = sorted(common_dates)
    matrix: List[List[float]] = []
    for obs_date in sorted_dates:
        row = [ticker_returns[ticker][obs_date] for ticker in tickers]
        matrix.append(row)

    return tickers, matrix


def compute_correlation_matrix(
    price_history: PriceHistory,
    *,
    return_type: str = "log",
) -> CorrelationResult:
    """Compute a correlation matrix from ``PriceHistory`` data."""

    tickers, matrix = _align_returns(price_history, return_type=return_type)
    n_observations = len(matrix)
    if n_observations < 2:
        raise ValueError("Not enough return observations to compute correlation.")

    columns = list(zip(*matrix))
    means = [mean(column) for column in columns]
    stdevs = [
        sqrt(sum((value - column_mean) ** 2 for value in column) / (n_observations - 1))
        for column, column_mean in zip(columns, means)
    ]

    correlation_matrix: List[List[float]] = []
    for i in range(len(tickers)):
        row: List[float] = []
        for j in range(len(tickers)):
            if i == j:
                row.append(1.0)
                continue

            std_i, std_j = stdevs[i], stdevs[j]
            if isclose(std_i, 0.0) or isclose(std_j, 0.0):
                row.append(0.0)
                continue

            covariance = sum(
                (matrix[k][i] - means[i]) * (matrix[k][j] - means[j]) for k in range(n_observations)
            ) / (n_observations - 1)
            correlation = covariance / (std_i * std_j)
            row.append(max(-1.0, min(1.0, correlation)))
        correlation_matrix.append(row)

    return CorrelationResult(tickers=tickers, matrix=correlation_matrix, observation_count=n_observations)


__all__ = ["CorrelationResult", "compute_returns", "compute_correlation_matrix"]
