"""Some useful Monadic functions.

This module contains some useful Monadic functions. Most functions
are extension methods to the Monad class, making them available to
subclasses that inherit from Monad.
"""

from __future__ import annotations

from collections.abc import Callable

from .typing import Monad


def compose[A, B, Result](f: Callable[[B], Result], g: Callable[[A], Monad[B, Result]]) -> Callable[[A], Result]:
    r"""Monadic compose function.

    Right-to-left Kleisli composition of two monadic functions.

    (<=<) :: Monad m => (b -> m c) -> (a -> m b) -> a -> m c
    f <=< g = \x -> g x >>= f
    """
    return lambda x: g(x).bind(f)
