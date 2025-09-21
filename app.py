"""Flask-based correlation heatmap builder."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from typing import List, Tuple

from flask import Flask, render_template, request

from correlheatmap.analysis import CorrelationResult, compute_correlation_matrix
from correlheatmap.data import fetch_daily_closes
from correlheatmap.visualization import correlation_to_hex

DEFAULT_LOOKBACK_DAYS = 365
DEFAULT_TICKERS = "AAPL, MSFT, GOOGL, NVDA"
RETURN_TYPES = ("log", "pct")

COLOR_SCALE = [
    [0.0, correlation_to_hex(-1.0)],
    [0.25, correlation_to_hex(-0.5)],
    [0.5, correlation_to_hex(0.0)],
    [0.75, correlation_to_hex(0.5)],
    [1.0, correlation_to_hex(1.0)],
]

app = Flask(__name__)


@dataclass
class FormState:
    tickers: str
    start: str
    end: str
    return_type: str


def _default_form_state() -> FormState:
    today = date.today()
    start = today - timedelta(days=DEFAULT_LOOKBACK_DAYS)
    return FormState(
        tickers=DEFAULT_TICKERS,
        start=start.isoformat(),
        end=today.isoformat(),
        return_type="log",
    )


def _parse_tickers(raw: str) -> List[str]:
    parts = [item.strip().upper() for item in raw.replace("\n", " ").replace(",", " ").split()]
    return [item for item in parts if item]


def _parse_date(raw: str, label: str) -> Tuple[date | None, str | None]:
    cleaned = raw.strip()
    if not cleaned:
        return None, f"{label.title()} date is required."
    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d").date()
    except ValueError:
        return None, f"Invalid {label} date: '{raw}'. Use YYYY-MM-DD."
    return parsed, None


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    form_state = _default_form_state()
    result: CorrelationResult | None = None
    error: str | None = None

    if request.method == "POST":
        form_state = FormState(
            tickers=request.form.get("tickers", form_state.tickers),
            start=request.form.get("start", form_state.start),
            end=request.form.get("end", form_state.end),
            return_type=request.form.get("return_type", form_state.return_type),
        )

        tickers = _parse_tickers(form_state.tickers)
        if len(tickers) < 2:
            error = "Enter at least two ticker symbols separated by spaces or commas."
        elif form_state.return_type not in RETURN_TYPES:
            error = "Return type must be 'log' or 'pct'."
        else:
            start_date, start_error = _parse_date(form_state.start, "start")
            end_date, end_error = _parse_date(form_state.end, "end")
            if start_error:
                error = start_error
            elif end_error:
                error = end_error
            elif start_date is None or end_date is None:
                error = "Both start and end dates are required."
            elif start_date >= end_date:
                error = "Start date must be earlier than end date."
            else:
                try:
                    price_history = fetch_daily_closes(tickers, start=start_date, end=end_date)
                    result = compute_correlation_matrix(
                        price_history, return_type=form_state.return_type
                    )
                except (ImportError, ValueError) as exc:
                    error = str(exc)
                except Exception as exc:  # pragma: no cover - defensive fallback
                    error = f"Unexpected error: {exc}"

    status_message = None
    table_rows = None
    if result is not None:
        status_message = (
            f"Computed correlations using {result.observation_count} overlapping daily returns."
        )
        table_rows = list(zip(result.tickers, result.matrix))

    return render_template(
        "index.html",
        form=asdict(form_state),
        result=result,
        error=error,
        status_message=status_message,
        table_rows=table_rows,
        return_types=RETURN_TYPES,
        color_scale=COLOR_SCALE,
        correlation_to_hex=correlation_to_hex,
    )


def create_app() -> Flask:
    """Return the configured Flask application for WSGI servers."""

    return app


if __name__ == "__main__":
    app.run(debug=True)
