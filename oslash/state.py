from typing import Callable, Tuple, Any, TypeVar, Generic

from .util import Unit
from .typing import Functor
from .typing import Monad

TState = TypeVar("TState")
TSource = TypeVar("TSource")
TResult = TypeVar("TResult")


class State(Generic[TSource, TState]):
    """The state monad.

    Wraps stateful computations. A stateful computation is a function
    that takes a state and returns a result and new state:

        state -> (result, state')
    """

    def __init__(self, fn: Callable[[TState], Tuple[TSource, TState]]) -> None:
        """Initialize a new state.

        Keyword arguments:
        fn -- State processor.
        """

        self._fn = fn

    @classmethod
    def unit(cls, value: TSource) -> "State[TSource, TState]":
        r"""Create new State.

        The unit function creates a new State object wrapping a stateful
        computation.

        State $ \s -> (x, s)
        """
        return cls(lambda state: (value, state))

    def map(self, mapper: Callable[[TSource], TResult]) -> "State[TResult, TState]":
        def _(a: Any, state: Any) -> Tuple[Any, Any]:
            return mapper(a), state

        return State(lambda state: _(*self.run(state)))

    def bind(self, fn: Callable[[TSource], "State[TState, TResult]"]) -> "State[TResult, TState]":
        r"""m >>= k = State $ \s -> let (a, s') = runState m s
        in runState (k a) s'
        """

        def _(result: Any, state: Any) -> Tuple[Any, Any]:
            return fn(result).run(state)

        return State(lambda state: _(*self.run(state)))

    @classmethod
    def get(cls) -> "State[TState, TState]":
        r"""get = state $ \s -> (s, s)"""
        return State(lambda state: (state, state))

    @classmethod
    def put(cls, new_state: TState) -> "State[Tuple, TState]":
        r"""put newState = state $ \s -> ((), newState)"""
        return State(lambda state: (Unit, new_state))

    def run(self, state: TState) -> Tuple[TSource, TState]:
        """Return wrapped state computation.

        This is the inverse of unit and returns the wrapped function.
        """
        return self._fn(state)

    def __call__(self, state: Any) -> Tuple:
        return self.run(state)


assert issubclass(State, Functor)
assert issubclass(State, Monad)
