from typing import Any, Callable, Tuple

from .util import Unit
from .abc import Functor
from .abc import Monad


class State(Monad, Functor):

    """The state monad.

    Wraps stateful computations. A stateful computation is a function
    that takes a state and returns a result and new state:

        state -> (result, state')
    """

    def __init__(self, fn: Callable[[Any], Tuple[Any, Any]]):
        """Initialize a new state.

        Keyword arguments:
        fn -- State processor.
        """

        self._get_value = lambda: fn

    @classmethod
    def unit(cls, value: Any) -> 'State':
        r"""Create new State.

        The unit function creates a new State object wrapping a stateful
        computation.

        State $ \s -> (x, s)
        """
        return cls(lambda state: (value, state))

    def map(self, mapper: Callable[[Any], Any]) -> 'State':
        def _(a, state):
            return mapper(a), state

        return State(lambda state: _(*self.run(state)))

    def bind(self, fn: Callable[[Any], 'State']) -> 'State':
        r"""m >>= k = State $ \s -> let (a, s') = runState m s
                         in runState (k a) s'
        """

        def _(result, state):
            return fn(result).run(state)

        return State(lambda state: _(*self.run(state)))

    @classmethod
    def get(cls) -> 'State':
        r"""get = state $ \s -> (s, s)"""
        return State(lambda state: (state, state))

    @classmethod
    def put(cls, new_state: Any) -> 'State':
        r"""put newState = state $ \s -> ((), newState)"""
        return State(lambda state: (Unit, new_state))

    def run(self, *args):
        """Return wrapped state computation.

        This is the inverse of unit and returns the wrapped function.
        If we receive args, we call the function directly to avoid the
        ugly `run()(args)` pattern.
        """
        return self._get_value()(*args) if args else self._get_value()

    def __call__(self, state):
        return self.run(state)

    def __eq__(self, other) -> bool:
        """Test if two stateful computations are equal.

        Not really possible unless we give both computations the same
        state to chew on."""

        state = 42  # Default state. Can't be wrong.
        return self(state) == other(state)
