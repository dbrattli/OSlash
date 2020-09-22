import unittest

from typing import Callable
from oslash import State
from oslash.util import identity, compose

# pure = State.pure
unit = State.unit
put = State.put
get = State.get

state = 42

class TestState(unittest.TestCase):

    def test_state_greeter(self) -> None:

        def greeter() -> State:
            state = get().bind(lambda name:
                               put("tintin").bind(
                                   lambda _: unit("hello, %s!" % name)))
            return state

        result = greeter().run("adit")
        self.assertEqual("hello, adit!", result[0])
        self.assertEqual("tintin", result[1])


class TestStateFunctor(unittest.TestCase):

    def test_state_functor_map(self) -> None:
        x : State[int, int] = unit(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.map(f).run(state),
            unit(420).run(state)
        )

    def test_state_functor_law_1(self) -> None:
        # fmap id = id
        x = unit(42)

        self.assertEqual(
            x.map(identity).run(state),
            x.run(state)
        )

    def test_state_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x + 10

        def g(x):
            return x * 10

        x : State[int, int] = unit(42)

        self.assertEqual(
            x.map(compose(f, g)).run(state),
            x.map(g).map(f).run(state)
        )


class TestStateMonad(unittest.TestCase):

    def test_state_monad_bind(self) -> None:
        m : State[int, int] = unit(42)
        f : Callable[[int], State[int, int]]= lambda x: unit(x * 10)

        self.assertEqual(
            m.bind(f).run(state),
            unit(420).run(state)
        )

    def test_state_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x + 100000)
        x = 3

        self.assertEqual(
            unit(x).bind(f).run(state),
            f(x).run(state)
        )

    def test_state_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m = unit("move on up")

        self.assertEqual(
            m.bind(unit).run(state),
            m.run(state)
        )

    def test_state_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = unit(42)
        f = lambda x: unit(x + 1000)
        g = lambda y: unit(y * 42)

        self.assertEqual(
            m.bind(f).bind(g).run(state),
            m.bind(lambda x: f(x).bind(g)).run(state)
        )
