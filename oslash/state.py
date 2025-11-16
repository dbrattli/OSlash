"""State monad implementation.

The State monad allows for stateful computations.
"""

from __future__ import annotations

from collections.abc import Callable

from .typing import Functor, Monad
from .util import Unit


class State[T, S]:
    """The state monad.

    Wraps stateful computations. A stateful computation is a function
    that takes a state and returns a result and new state:

        state -> (result, state')
    """

    def __init__(self, fn: Callable[[S], tuple[T, S]]) -> None:
        """Initialize a new state.

        Args:
            fn: State processor function
        """
        self._fn = fn

    @classmethod
    def unit(cls, value: T) -> State[T, S]:
        r"""Create new State.

        The unit function creates a new State object wrapping a stateful
        computation.

        State $ \s -> (x, s)
        """
        return cls(lambda state: (value, state))

    def map[U](self, mapper: Callable[[T], U]) -> State[U, S]:
        """Map a function over the State value."""

        def transform(a: T, state: S) -> tuple[U, S]:
            return mapper(a), state

        return State(lambda state: transform(*self.run(state)))

    def bind[U](self, fn: Callable[[T], State[U, S]]) -> State[U, S]:
        r"""Bind a monadic function.

        m >>= k = State $ \s -> let (a, s') = runState m s
        in runState (k a) s'
        """

        def transform(result: T, state: S) -> tuple[U, S]:
            return fn(result).run(state)

        return State(lambda state: transform(*self.run(state)))

    @classmethod
    def get(cls) -> State[S, S]:
        r"""Get the state.

        get = state $ \s -> (s, s)
        """
        return State(lambda state: (state, state))

    @classmethod
    def put(cls, new_state: S) -> State[tuple[()], S]:
        r"""Put (set) the state.

        put newState = state $ \s -> ((), newState)
        """
        return State(lambda state: (Unit, new_state))

    def run(self, state: S) -> tuple[T, S]:
        """Return wrapped state computation.

        This is the inverse of unit and returns the wrapped function.
        """
        return self._fn(state)

    def __call__(self, state: S) -> tuple[T, S]:
        """Call the state computation with given state."""
        return self.run(state)


# Type assertions for runtime checking
assert issubclass(State, Functor)
assert issubclass(State, Monad)
