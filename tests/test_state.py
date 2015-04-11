import unittest

from oslash import State
from oslash.util import identity, compose, compose2

#pure = State.pure
unit = State.unit
put = State.put
get = State.get


class TestState(unittest.TestCase):
    def test_state_greeter(self):

        def greeter() -> State:
            state = get().bind(lambda name:
                               put("tintin").bind(
                                   lambda _: unit("hello, %s!" % name)))
            return state

        result = greeter().run()("adit")
        self.assertEqual("hello, adit!", result[0])
        self.assertEqual("tintin", result[1])


class TestStateFunctor(unittest.TestCase):

    def test_state_functor_map(self):
        x = unit(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.map(f),
            unit(420)
        )

    def test_state_functor_law_1(self):
        # fmap id = id
        x = unit(42)

        self.assertEqual(
            x.map(identity),
            x
        )

    def test_state_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = unit(42)

        self.assertEquals(
            x.map(compose(f, g)),
            x.map(g).map(f)
        )


class TestStateMonad(unittest.TestCase):

    def test_state_monad_bind(self):
        m = unit(42)
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            unit(420)
        )

    def test_state_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x+100000)
        x = 3

        self.assertEqual(
            unit(x).bind(f),
            f(x)
        )

    def test_state_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = unit("move on up")

        self.assertEqual(
            m.bind(unit),
            m
        )

    def test_state_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = unit(42)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )
