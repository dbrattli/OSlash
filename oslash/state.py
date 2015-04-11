from typing import Any, Callable, Tuple

from .util import Unit
from .abc import Functor
from .abc import Monad
# from .monoid import Monoid


class State(Monad, Functor):

    """The state monad.

    Wraps stateful computations.
    """

    def __init__(self, fn: Callable[[Any], Tuple[Any, Any]]):
        """Initialize a new state.

        Keyword arguments:
        fn -- State processor.
        """

        self._get_value = lambda: fn

    @classmethod
    def unit(cls, value: Any) -> 'State':
        """The return function creates a State.

        State $ \s -> (x, s)
        """
        return cls(lambda state: (value, state))

    def map(self, mapper: Callable[[Any], Any]) -> 'State':
        def _(a, state):
            return mapper(a), state

        return State(lambda state: _(*self.run()(state)))

    def bind(self, fn: Callable[[Any], 'State']) -> 'State':
        """m >>= k = State $ \s -> let (a, s') = runState m s
                         in runState (k a) s'
        """

        def _(a, state):
            return fn(a).run()(state)

        return State(lambda state: _(*self.run()(state)))

    @classmethod
    def get(cls) -> 'State':
        """get = state $ \s -> (s, s)"""
        return State(lambda state: (state, state))

    @classmethod
    def put(cls, new_state: Any) -> 'State':
        """put newState = state $ \s -> ((), newState)"""
        return State(lambda state: (Unit, new_state))

    def run(self):
        return self._get_value()

    def __call__(self, state):
        return self.run()(state)

    def __eq__(self, other) -> bool:
        state = 42  # Default state
        return self(state) == other(state)
