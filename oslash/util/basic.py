"""Basic utility functions and constants."""

from __future__ import annotations

# Unit type - represents the absence of a meaningful value
Unit: tuple[()] = ()


def indent(level: int, size: int = 2) -> str:
    """Return indentation string.

    Args:
        level: The indentation level
        size: The number of spaces per level

    Returns:
        String of spaces for indentation
    """
    return " " * level * size
