"""Apply a callable or explicitly curry one missing argument."""

from collections.abc import Callable
from functools import partial
from inspect import signature
from typing import Any


def apply_callable(func: Callable[..., Any], value: object) -> Any:
    """Apply a unary callable, or bind the first argument of a multi-arg callable.

    Inspect arity after a TypeError so one raised inside a unary function
    is not mistaken for a request to curry it.
    """
    try:
        return func(value)
    except TypeError:
        try:
            callable_signature = signature(func)
        except (TypeError, ValueError):
            # Some built-ins accept more arguments but have no inspectable signature.
            return partial(func, value)

        try:
            callable_signature.bind(value)
        except TypeError:
            return partial(func, value)
        raise
