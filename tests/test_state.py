import unittest
from collections.abc import Callable

from oslash import State
from oslash.util import compose, identity

state = 42


class TestState(unittest.TestCase):
    def test_state_greeter(self) -> None:
        def greeter() -> State[str, str]:
            return State.get().bind(lambda name: State.put("tintin").bind(lambda _: State.unit(f"hello, {name}!")))

        result = greeter().run("adit")
        assert result[0] == "hello, adit!"
        assert result[1] == "tintin"


class TestStateFunctor(unittest.TestCase):
    def test_state_functor_map(self) -> None:
        x: State[int, int] = State.unit(42)
        f: Callable[[int], int] = lambda x: x * 10

        assert x.map(f).run(state) == State.unit(420).run(state)

    def test_state_functor_law_1(self) -> None:
        # fmap id = id
        x: State[int, int] = State.unit(42)

        assert x.map(identity).run(state) == x.run(state)

    def test_state_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        f: Callable[[int], int] = lambda x: x + 10
        g: Callable[[int], int] = lambda x: x * 10

        x: State[int, int] = State.unit(42)

        assert x.map(compose(f, g)).run(state) == x.map(g).map(f).run(state)


class TestStateMonad(unittest.TestCase):
    def test_state_monad_bind(self) -> None:
        m: State[int, int] = State.unit(42)
        f: Callable[[int], State[int, int]] = lambda x: State.unit(x * 10)

        assert m.bind(f).run(state) == State.unit(420).run(state)

    def test_state_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f: Callable[[int], State[int, int]] = lambda x: State.unit(x + 100000)
        x: int = 3

        assert State.unit(x).bind(f).run(state) == f(x).run(state)

    def test_state_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m: State[str, str] = State.unit("move on up")

        assert m.bind(State.unit).run(state) == m.run(state)

    def test_state_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m: State[int, int] = State.unit(42)
        f: Callable[[int], State[int, int]] = lambda x: State.unit(x + 1000)
        g: Callable[[int], State[int, int]] = lambda y: State.unit(y * 42)

        assert m.bind(f).bind(g).run(state) == m.bind(lambda x: f(x).bind(g)).run(state)
