"""Type protocols for functional programming abstractions."""

from __future__ import annotations

from .applicative import Applicative
from .functor import Functor
from .monad import Monad
from .monoid import Monoid

__all__ = ["Applicative", "Functor", "Monad", "Monoid"]
