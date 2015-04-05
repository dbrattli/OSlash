# coding=utf-8
import unittest

from oslash.maybe import Maybe, Just, Nothing
from oslash.util import identity, compose, compose2

pure = Just.pure
return_ = Just.return_


class TestMaybeFunctor(unittest.TestCase):
    def test_just_functor_fmap(self):
        f = lambda x: x*2
        x = Just(21)

        self.assertEquals(
            x.fmap(f),
            Just(42)
        )

    def test_nothing_functor_fmap(self):
        f = lambda x: x+2
        x = Nothing()

        self.assertEquals(
            x.fmap(f),
            x
        )

    def test_nothing_functor_law1(self):
        # fmap id = id
        self.assertEquals(
            Nothing().fmap(identity),
            Nothing()
        )

    def test_just_functor_law1(self):
        # fmap id = id
        x = Just(3)
        self.assertEquals(
            x.fmap(identity),
            x
        )

    def test_just_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = Just(42)

        self.assertEquals(
            x.fmap(compose(f, g)),
            x.fmap(g).fmap(f)
        )

    def test_nothing_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = Nothing()

        self.assertEquals(
            x.fmap(compose(f, g)),
            x.fmap(g).fmap(f)
        )


class TestMaybeApplicative(unittest.TestCase):

    def test_just_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        x = return_(42)
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(x),
            x.fmap(f)
        )

    def test_nothing_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        x = Nothing()
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(x),
            x.fmap(f)
        )

    def test_just_applicative_law_identity(self):
        # pure id <*> v = v
        v = return_(42)

        self.assertEquals(
            pure(identity).apply(v),
            v
        )

    def test_nothing_applicative_law_identity(self):
        # pure id <*> v = v
        v = Nothing()

        self.assertEquals(
            pure(identity).apply(v),
            v
        )

    def test_just_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = return_(42)
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEquals(
            pure(compose2).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_identity_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = Nothing()
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEquals(
            pure(compose2).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_just_applicative_law_homomorphism(self):
        # pure f <*> pure x = pure (f x)
        x = 42
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(pure(x)),
            pure(f(x))
        )

    def test_nothing_applicative_law_homomorphism(self):
        # pure f <*> pure x = pure (f x)
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(Nothing()),
            Nothing()
        )

    def test_just_applicative_law_interchange(self):
        # u <*> pure y = pure ($ y) <*> u

        y = 43
        u = return_(lambda x: x*42)

        self.assertEquals(
            u.apply(pure(y)),
            pure(lambda f: f(y)).apply(u)
        )

    def test_nothing_applicative_law_interchange(self):
        # u <*> pure y = pure ($ y) <*> u

        u = return_(lambda x: x*42)

        self.assertEquals(
            u.apply(Nothing()),
            Nothing().apply(u)
        )

    def test_just_applicative_1(self):
        a = Just.pure(lambda x, y: x+y).apply(Just(2)).apply(Just(40))
        self.assertNotEquals(a, Nothing())
        self.assertEquals(a, Just(42))

    def test_just_applicative_2(self):
        a = Just.pure(lambda x, y: x+y).apply(Nothing()).apply(Just(42))
        self.assertEquals(a, Nothing())

    def test_just_applicative_3(self):
        a = Just.pure(lambda x, y: x+y).apply(Just(42)).apply(Nothing())
        self.assertEquals(a, Nothing())


class TestMaybeMonoid(unittest.TestCase):

    def test_maybe_monoid_nothing_mappend_just(self):
        a = Nothing().mappend(Just("Python"))
        self.assertEquals(a, Just("Python"))

    def test_maybe_monoid_just_mappend_nothing(self):
        a = Just("Python").mappend(Nothing())
        self.assertEquals(a, Just("Python"))

    def test_maybe_monoid_just_mappend_just(self):
        a = Just("Python").mappend(Just(" rocks!"))
        self.assertEquals(a, Just("Python rocks!"))

    def test_maybe_monoid_mconcat(self):
        a = Maybe.mconcat([Just(2), Just(40)])
        self.assertEquals(a, Just(42))


class TestMaybeMonad(unittest.TestCase):

    def test_just_monad_bind(self):
        m = return_(42)
        f = lambda x: return_(x*10)

        self.assertEqual(
            m.bind(f),
            return_(420)
        )

    def test_nothing_monad_bind(self):
        m = Nothing()
        f = lambda x: return_(x*10)

        self.assertEqual(
            m.bind(f),
            Nothing()
        )

    def test_just_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: return_(x+100000)
        x = 3

        self.assertEqual(
            return_(x).bind(f),
            f(x)
        )

    def test_nothing_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: return_(x+100000)

        self.assertEqual(
            Nothing().bind(f),
            Nothing()
        )

    def test_just_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = return_("move on up")

        self.assertEqual(
            m.bind(return_),
            m
        )

    def test_nothing_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = Nothing()

        self.assertEqual(
            m.bind(return_),
            m
        )

    def test_just_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = return_(42)
        f = lambda x: return_(x+1000)
        g = lambda y: return_(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )

    def test_nothing_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = Nothing()
        f = lambda x: return_(x+1000)
        g = lambda y: return_(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )
