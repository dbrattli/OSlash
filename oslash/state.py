from typing import TypeVar, Callable, Tuple, Generic

from .util import Unit
from .abc import Functor
from .abc import Monad

A = TypeVar('A')  # Type of value
B = TypeVar('B')  # Type of new value
S = TypeVar('S')  # Type of state


class State(Generic[A, S], Monad[A], Functor[A]):

    """The state monad.

    Wraps stateful computations. A stateful computation is a function
    that takes a state and returns a result and new state:

        state -> (result, state')
    """

    def __init__(self, fn: Callable[[S], Tuple[A, S]]) -> None:
        """Initialize a new state.

        Keyword arguments:
        fn -- State processor.
        """

        self._value = fn

    @classmethod
    def unit(cls, value: A) -> 'State[A, S]':
        r"""Create new State.

        The unit function creates a new State object wrapping a stateful
        computation.

        State $ \s -> (x, s)
        """
        return cls(lambda state: (value, state))

    def map(self, mapper: Callable[[A], B]) -> 'State[B, S]':
        def _(a: A, state: S) -> Tuple[B, S]:
            return mapper(a), state

        return State(lambda state: _(*self.run(state)))

    def bind(self, fn: Callable[[A], 'State[B, S]']) -> 'State[B, S]':
        r"""m >>= k = State $ \s -> let (a, s') = runState m s
                         in runState (k a) s'
        """

        def _(result: A, state: S) -> Tuple[B, S]:
            return fn(result).run(state)

        return State(lambda state: _(*self.run(state)))

    @classmethod
    def get(cls) -> 'State[S, S]':
        r"""get = state $ \s -> (s, s)"""
        return State(lambda state: (state, state))

    @classmethod
    def put(cls, new_state: S) -> 'State[A, S]':
        r"""put newState = state $ \s -> ((), newState)"""
        return State(lambda state: (Unit, new_state))

    def run(self, state: S) -> Tuple[A, S]:
        """Return wrapped state computation.

        This is the inverse of unit and returns the wrapped function.
        """
        return self._value(state)

    def __call__(self, state: S) -> Tuple[A, S]:
        return self.run(state)

    def __eq__(self, other) -> bool:
        """Test if two stateful computations are equal.

        Not really possible unless we give both computations the same
        state to chew on."""

        state = 42  # Default state. Can't be wrong.
        return self(state) == other(state)
