from __future__ import annotations

from correlheatmap.visualization import correlation_to_hex


def test_correlation_to_hex_range() -> None:
    assert correlation_to_hex(-1.0) == "#2166ac"
    assert correlation_to_hex(1.0) == "#b2182b"
    assert correlation_to_hex(0.0) == "#f7f7f7"


def test_correlation_to_hex_clamps_values() -> None:
    assert correlation_to_hex(-2.0) == "#2166ac"
    assert correlation_to_hex(2.0) == "#b2182b"
