# coding=utf-8
import unittest

from oslash.maybe import Maybe, Just, Nothing
from oslash.util import identity, compose, fmap

pure = Just.pure
unit = Just.unit


class TestMaybeFunctor(unittest.TestCase):
    def test_just_functor_map(self):
        f = lambda x: x * 2
        x = Just(21)

        self.assertEqual(
            x.map(f),
            Just(42)
        )

    def test_nothing_functor_map(self):
        f = lambda x: x + 2
        x = Nothing()

        self.assertEqual(
            x.map(f),
            x
        )

    def test_nothing_functor_law1(self):
        # fmap id = id
        self.assertEqual(
            Nothing().map(identity),
            Nothing()
        )

    def test_just_functor_law1(self):
        # fmap id = id
        x = Just(3)
        self.assertEqual(
            x.map(identity),
            x
        )

    def test_just_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x + 10

        def g(x):
            return x * 10

        x = Just(42)

        self.assertEqual(
            x.map(compose(f, g)),
            x.map(g).map(f)
        )

    def test_nothing_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = Nothing()

        self.assertEqual(
            x.map(compose(f, g)),
            x.map(g).map(f)
        )


class TestMaybeApplicative(unittest.TestCase):

    def test_just_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        x = unit(42)
        f = lambda x: x * 42

        self.assertEqual(
            pure(f).apply(x),
            x.map(f)
        )

    def test_nothing_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        x = Nothing()
        f = lambda x: x * 42

        self.assertEqual(
            pure(f).apply(x),
            x.map(f)
        )

    def test_just_applicative_law_identity(self):
        # pure id <*> v = v
        v = unit(42)

        self.assertEqual(
            pure(identity).apply(v),
            v
        )

    def test_nothing_applicative_law_identity(self):
        # pure id <*> v = v
        v = Nothing()

        self.assertEqual(
            pure(identity).apply(v),
            v
        )

    def test_just_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = unit(42)
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEqual(
            pure(fmap).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_identity_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = Nothing()
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEqual(
            pure(fmap).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_just_applicative_law_homomorphism(self):
        # pure f <*> pure x = pure (f x)
        x = 42
        f = lambda x: x * 42

        self.assertEqual(
            pure(f).apply(pure(x)),
            pure(f(x))
        )

    def test_nothing_applicative_law_homomorphism(self):
        # pure f <*> pure x = pure (f x)
        f = lambda x: x * 42

        self.assertEqual(
            pure(f).apply(Nothing()),
            Nothing()
        )

    def test_just_applicative_law_interchange(self):
        # u <*> pure y = pure ($ y) <*> u

        y = 43
        u = unit(lambda x: x*42)

        self.assertEqual(
            u.apply(pure(y)),
            pure(lambda f: f(y)).apply(u)
        )

    def test_nothing_applicative_law_interchange(self):
        # u <*> pure y = pure ($ y) <*> u

        u = unit(lambda x: x*42)

        self.assertEqual(
            u.apply(Nothing()),
            Nothing().apply(u)
        )

    def test_just_applicative_1(self):
        a = Just.pure(lambda x, y: x+y).apply(Just(2)).apply(Just(40))
        self.assertNotEqual(a, Nothing())
        self.assertEqual(a, Just(42))

    def test_just_applicative_2(self):
        a = Just.pure(lambda x, y: x+y).apply(Nothing()).apply(Just(42))
        self.assertEqual(a, Nothing())

    def test_just_applicative_3(self):
        a = Just.pure(lambda x, y: x+y).apply(Just(42)).apply(Nothing())
        self.assertEqual(a, Nothing())


class TestMaybeMonoid(unittest.TestCase):

    def test_maybe_monoid_nothing_append_just(self):
        m = Just("Python")

        self.assertEqual(
            Nothing() + m,
            m
        )

    def test_maybe_monoid_just_append_nothing(self):
        m = Just("Python")

        self.assertEqual(
            m + Nothing(),
            m
        )

    def test_maybe_monoid_just_append_just(self):
        m = Just("Python")
        n = Just(" rocks!")

        self.assertEqual(
            m + n,
            Just("Python rocks!")
        )

    def test_maybe_monoid_concat(self):

        self.assertEqual(
            Maybe.concat([Just(2), Just(40)]),
            Just(42)
        )


class TestMaybeMonad(unittest.TestCase):

    def test_just_monad_bind(self):
        m = unit(42)
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            unit(420)
        )

    def test_nothing_monad_bind(self):
        m = Nothing()
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            Nothing()
        )

    def test_just_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x+100000)
        x = 3

        self.assertEqual(
            unit(x).bind(f),
            f(x)
        )

    def test_nothing_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x+100000)

        self.assertEqual(
            Nothing().bind(f),
            Nothing()
        )

    def test_just_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = unit("move on up")

        self.assertEqual(
            m.bind(unit),
            m
        )

    def test_nothing_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = Nothing()

        self.assertEqual(
            m.bind(unit),
            m
        )

    def test_just_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = unit(42)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )

    def test_nothing_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = Nothing()
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )

    def test_combine_just_and_just_rule1(self):
        self.assertEqual(
            Just(5) and Just(6),
            Just(6)
        )

    def test_combine_just_and_just_rule2(self):
        self.assertEqual(
            Just(0) and Just(6),
            Just(0)
        )

    def test_combine_just_or_nothing_rule1(self):
        self.assertEqual(
            Just(5) or Nothing,
            Just(5)
        )

    def test_combine_just_or_nothing_rule2(self):
        self.assertEqual(
            Just(0) or Nothing,
            Nothing
        )
