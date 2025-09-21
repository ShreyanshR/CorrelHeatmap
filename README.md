# Correlation Heatmap Builder

An interactive web application for exploring how equity tickers move together. Enter a basket of
symbols, download daily closes from Yahoo Finance via `yfinance`, and inspect the resulting
correlation matrix as both a Plotly heatmap and a colour-coded data table.

## Features

- Flask UI with a responsive form, error handling, and live Plotly heatmap rendering
- Pure-Python analytics layer for return and correlation calculations (log or percent returns)
- Optional integration with `yfinance` for historical price retrieval
- Accessible table view that mirrors the heatmap colours for quick inspection and export

## Getting Started

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> The analytical code itself depends only on the Python standard library. `Flask`, `plotly`, and
> `yfinance` power the optional web interface and data download features.

### 3. Run the development server

```bash
flask --app app run --debug
```

Open <http://127.0.0.1:5000/> in your browser. Provide ticker symbols (separated by commas, spaces,
or new lines), choose a date range and return type, and select **Build heatmap**. The app fetches
prices, computes overlapping return series, and renders the correlation heatmap alongside the
numeric matrix and observation count.

> You can alternatively launch the app with `python app.py` if you prefer not to use the Flask CLI.

## Running Tests

A pytest suite verifies the return calculation, correlation assembly, and colour mapping utilities:

```bash
pytest
```

## Project Structure

```
CorrelHeatmap/
├── app.py                 # Flask application with routing and request handling
├── requirements.txt       # Optional runtime dependencies
├── templates/
│   └── index.html         # UI layout, styling, and Plotly heatmap wiring
├── src/
│   └── correlheatmap/
│       ├── __init__.py
│       ├── analysis.py    # Pure Python return/correlation calculations
│       ├── data.py        # Optional yfinance data loader
│       └── visualization.py  # Colour utilities for the heatmap
└── tests/                 # Pytest unit tests
```

## Notes

- Network access is required for live data downloads. If you are offline, construct a
  `PriceHistory` dictionary manually and call `compute_correlation_matrix` to drive the template.
- Heatmap colours follow a blue (negative) to red (positive) gradient with white representing zero
  correlation. Values are clamped to the [-1, 1] interval.
- The Flask app exposes a `create_app` factory for easy deployment to production servers if needed.
