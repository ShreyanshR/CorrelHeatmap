# Correlation Heatmap Builder

A desktop application for exploring the historical correlations between equity tickers. Enter a
portfolio, download end-of-day prices from Yahoo Finance (via `yfinance`), and visualise the
correlation matrix as a colour-coded Tkinter canvas.

## Features

- Pure-Python correlation engine requiring only the standard library for analysis
- Optional integration with `yfinance` to download daily adjusted closes
- Custom Tkinter canvas heatmap with numeric overlays and tabular output
- Supports log or percentage return calculations and enforces simple input validation

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

> `yfinance` pulls in `pandas` and other dependencies needed for data retrieval. The analytical code
> itself does not rely on external libraries.

### 3. Launch the Tkinter app

```bash
python app.py
```

Enter ticker symbols (comma or space separated), configure the date range and return calculation,
then press **Build heatmap**. The app fetches daily prices, computes overlapping return series, and
displays the resulting correlation matrix both numerically and as a colour map.

## Running Tests

A small pytest suite verifies the return and correlation calculations and the colour mapping logic:

```bash
pytest
```

## Project Structure

```
CorrelHeatmap/
├── app.py                 # Tkinter user interface and heatmap renderer
├── requirements.txt       # Optional runtime dependencies
├── src/
│   └── correlheatmap/
│       ├── __init__.py
│       ├── analysis.py    # Pure Python return/correlation calculations
│       ├── data.py        # Optional yfinance data loader
│       └── visualization.py  # Colour utilities for the heatmap
└── tests/                 # Pytest unit tests
```

## Notes

- Network access is required for live data downloads. If you are working offline, you can populate a
  `PriceHistory` dictionary manually and call `compute_correlation_matrix` directly.
- Heatmap colours follow a blue (negative) to red (positive) gradient with white representing zero
  correlation. Values are clamped to the [-1, 1] interval.
- Tkinter is part of the Python standard library, so no additional GUI framework is required.
