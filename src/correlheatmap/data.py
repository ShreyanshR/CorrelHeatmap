"""Utilities for retrieving historical price data."""

from __future__ import annotations

from datetime import date
from typing import Dict, Iterable, List, Sequence, Tuple

PricePoint = Tuple[date, float]
PriceHistory = Dict[str, List[PricePoint]]


def _normalise_tickers(tickers: Iterable[str]) -> List[str]:
    seen: set[str] = set()
    cleaned: List[str] = []
    for ticker in tickers:
        symbol = ticker.strip().upper()
        if symbol and symbol not in seen:
            cleaned.append(symbol)
            seen.add(symbol)
    return cleaned


def fetch_daily_closes(
    tickers: Sequence[str],
    *,
    start: date | None = None,
    end: date | None = None,
) -> PriceHistory:
    """Download daily adjusted closing prices via the optional :mod:`yfinance` dependency."""

    normalised = _normalise_tickers(tickers)
    if not normalised:
        raise ValueError("At least one ticker symbol must be provided.")

    try:
        import yfinance as yf  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised only when dependency missing at runtime
        raise ImportError(
            "The 'yfinance' package is required to download market data. Install it with 'pip install yfinance'."
        ) from exc

    history: PriceHistory = {}
    for symbol in normalised:
        data = yf.download(  # type: ignore[attr-defined]
            symbol,
            start=start,
            end=end,
            progress=False,
            auto_adjust=True,
            actions=False,
            interval="1d",
        )
        if data.empty:
            continue

        closes = []
        for index, value in data["Close"].items():  # type: ignore[index]
            closes.append((index.date(), float(value)))
        if closes:
            history[symbol] = closes

    if not history:
        raise ValueError("No price data was retrieved for the requested tickers.")
    return history


__all__ = ["fetch_daily_closes", "PriceHistory", "PricePoint"]
