"""Tkinter-based correlation heatmap builder."""

from __future__ import annotations

import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk
from typing import List

from correlheatmap.analysis import CorrelationResult, compute_correlation_matrix
from correlheatmap.data import fetch_daily_closes
from correlheatmap.visualization import correlation_to_hex

DEFAULT_LOOKBACK_DAYS = 365
CELL_SIZE = 70
LABEL_OFFSET = 90
FONT = ("Helvetica", 11)


class HeatmapApp:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Correlation Heatmap Builder")
        self.master.geometry("900x700")

        self.tickers_var = tk.StringVar(value="AAPL, MSFT, GOOGL, NVDA")
        today = date.today()
        self.start_var = tk.StringVar(value=(today - timedelta(days=DEFAULT_LOOKBACK_DAYS)).isoformat())
        self.end_var = tk.StringVar(value=today.isoformat())
        self.return_var = tk.StringVar(value="log")

        self._build_controls()
        self._build_results_area()

    def _build_controls(self) -> None:
        controls = ttk.Frame(self.master, padding=10)
        controls.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(controls, text="Tickers (comma separated):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(controls, textvariable=self.tickers_var, width=50).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(controls, text="Start date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(controls, textvariable=self.start_var, width=20).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(controls, text="End date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(controls, textvariable=self.end_var, width=20).grid(row=2, column=1, sticky=tk.W)

        ttk.Label(controls, text="Return type:").grid(row=3, column=0, sticky=tk.W)
        ttk.Combobox(
            controls,
            textvariable=self.return_var,
            values=("log", "pct"),
            width=5,
            state="readonly",
        ).grid(row=3, column=1, sticky=tk.W)

        ttk.Button(controls, text="Build heatmap", command=self.build_heatmap).grid(row=0, column=2, rowspan=2, padx=10)

        for i in range(3):
            controls.rowconfigure(i, pad=5)
        controls.columnconfigure(1, weight=1)

    def _build_results_area(self) -> None:
        results = ttk.Frame(self.master, padding=(10, 0, 10, 10))
        results.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(results, background="white", width=600, height=400)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.table = ttk.Treeview(results, show="headings", height=5)
        self.table.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.status_var = tk.StringVar(value="Enter tickers and click 'Build heatmap'.")
        ttk.Label(results, textvariable=self.status_var).pack(side=tk.TOP, anchor=tk.W)

    def build_heatmap(self) -> None:
        tickers = self._parse_tickers(self.tickers_var.get())
        if len(tickers) < 2:
            messagebox.showerror("Validation error", "Enter at least two ticker symbols.")
            return

        start_date = self._parse_date(self.start_var.get(), "start")
        end_date = self._parse_date(self.end_var.get(), "end")
        if start_date is None or end_date is None:
            return
        if start_date >= end_date:
            messagebox.showerror("Validation error", "Start date must be earlier than end date.")
            return

        try:
            price_history = fetch_daily_closes(tickers, start=start_date, end=end_date)
        except Exception as exc:
            messagebox.showerror("Data error", f"Unable to download prices: {exc}")
            return

        try:
            result = compute_correlation_matrix(price_history, return_type=self.return_var.get())
        except ValueError as exc:
            messagebox.showerror("Analysis error", str(exc))
            return

        self.status_var.set(
            f"Computed correlations using {result.observation_count} overlapping daily returns."
        )
        self._render_heatmap(result)
        self._render_table(result)

    def _render_heatmap(self, result: CorrelationResult) -> None:
        tickers = result.tickers
        size = CELL_SIZE
        offset = LABEL_OFFSET
        width = offset + size * len(tickers)
        height = offset + size * len(tickers)
        self.canvas.config(width=width, height=height)
        self.canvas.delete("all")

        for idx, ticker in enumerate(tickers):
            x = offset + idx * size + size / 2
            y = offset / 2
            self.canvas.create_text(x, y, text=ticker, angle=90, font=FONT)
            self.canvas.create_text(offset / 2, offset + idx * size + size / 2, text=ticker, font=FONT)

        for row_idx, row in enumerate(result.matrix):
            for col_idx, value in enumerate(row):
                x0 = offset + col_idx * size
                y0 = offset + row_idx * size
                x1 = x0 + size
                y1 = y0 + size
                colour = correlation_to_hex(value)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=colour, outline="white")
                self.canvas.create_text(
                    (x0 + x1) / 2,
                    (y0 + y1) / 2,
                    text=f"{value:.2f}",
                    font=FONT,
                )

    def _render_table(self, result: CorrelationResult) -> None:
        tickers = result.tickers
        columns = ["Ticker"] + tickers
        self.table.configure(columns=columns)
        for column in columns:
            anchor = "w" if column == "Ticker" else "center"
            width = 120 if column == "Ticker" else 80
            self.table.heading(column, text=column if column != "Ticker" else "")
            self.table.column(column, width=width, anchor=anchor)

        for row in self.table.get_children():
            self.table.delete(row)

        for ticker, values in zip(tickers, result.matrix):
            formatted = [f"{value:.2f}" for value in values]
            self.table.insert("", tk.END, values=[ticker] + formatted)

    @staticmethod
    def _parse_tickers(raw: str) -> List[str]:
        parts = [item.strip().upper() for item in raw.replace("\n", " ").replace(",", " ").split()]
        return [item for item in parts if item]

    @staticmethod
    def _parse_date(raw: str, label: str) -> date | None:
        try:
            parsed = datetime.strptime(raw.strip(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Validation error", f"Invalid {label} date: {raw}")
            return None
        return parsed


def main() -> None:
    root = tk.Tk()
    HeatmapApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
