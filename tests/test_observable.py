import unittest

from oslash.observable import Observable
from oslash.util import identity, compose

# pure = Cont.pure
unit = Observable.unit
just = Observable.just
call_cc = Observable.call_cc


class TestObservable(unittest.TestCase):
    def test_observable_just(self):
        stream = Observable.just(42)

        def on_next(x):
            return "OnNext(%s)" % x

        self.assertEqual("OnNext(42)", stream.subscribe(on_next))

    def test_observable_just_map(self):
        stream = Observable.just(42).map(lambda x: x*10)

        def on_next(x):
            return "OnNext(%s)" % x

        self.assertEqual("OnNext(420)", stream.subscribe(on_next))

    def test_observable_just_flatmap(self):
        stream = Observable.just(42).flat_map(lambda x: just(x*10))

        def on_next(x):
            return "OnNext(%s)" % x

        self.assertEqual("OnNext(420)", stream.subscribe(on_next))

    def test_observable_filter(self):
        stream = Observable.just(42).filter(lambda x: x < 100)
        xs = []

        def on_next(x):
            xs.append("OnNext(%s)" % x)
        stream.subscribe(on_next)
        self.assertEqual(["OnNext(42)"], xs)

    def test_cont_call_cc(self):
        f = lambda x: just(x*3)
        g = lambda x: just(x-2)

        def h(x, on_next):
            return f(x) if x == 5 else on_next(-1)

        stream = just(5) | (
            lambda x: call_cc(lambda on_next: h(x, on_next))) | (
                lambda y: g(y))

        on_next = lambda x: "Done: %s" % x

        self.assertEqual(
            "Done: 13",
            stream.subscribe(on_next)
        )


class TestObservableFunctor(unittest.TestCase):

    def test_cont_functor_map(self):
        x = unit(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.map(f),
            unit(420)
        )

    def test_cont_functor_law_1(self):
        # fmap id = id
        x = unit(42)

        self.assertEqual(
            x.map(identity),
            x
        )

    def test_cont_functor_law2(self):
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


class TestObservableMonad(unittest.TestCase):

    def test_cont_monad_bind(self):
        m = unit(42)
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            unit(420)
        )

    def test_cont_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x+100000)
        x = 3

        self.assertEqual(
            unit(x).bind(f),
            f(x)
        )

    def test_cont_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = unit("move on up")

        self.assertEqual(
            m.bind(unit),
            m
        )

    def test_cont_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = unit(42)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )
