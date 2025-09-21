"""Colour utilities for rendering correlation heatmaps on a Tkinter canvas."""

from __future__ import annotations

from typing import Tuple

NEGATIVE_COLOUR = (33, 102, 172)  # Deep blue
NEUTRAL_COLOUR = (247, 247, 247)  # Light grey
POSITIVE_COLOUR = (178, 24, 43)   # Deep red


def _interpolate_colour(start: Tuple[int, int, int], end: Tuple[int, int, int], fraction: float) -> str:
    fraction = max(0.0, min(1.0, fraction))
    red = int(start[0] + (end[0] - start[0]) * fraction + 0.5)
    green = int(start[1] + (end[1] - start[1]) * fraction + 0.5)
    blue = int(start[2] + (end[2] - start[2]) * fraction + 0.5)
    return f"#{red:02x}{green:02x}{blue:02x}"


def correlation_to_hex(value: float) -> str:
    """Map a correlation value in [-1, 1] to a colour hex code."""

    clamped = max(-1.0, min(1.0, value))
    if clamped >= 0:
        return _interpolate_colour(NEUTRAL_COLOUR, POSITIVE_COLOUR, clamped)
    return _interpolate_colour(NEGATIVE_COLOUR, NEUTRAL_COLOUR, 1.0 + clamped)


__all__ = ["correlation_to_hex"]
