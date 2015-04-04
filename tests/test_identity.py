# coding=utf-8
import unittest

from oslash.identity import Identity
from oslash.util import identity, compose, compose2


class TestIdentityFunctor(unittest.TestCase):

    def test_identity_functor_fmap(self):
        x = Identity(42)

        self.assertEqual(
            x.fmap(lambda x: x * 10),
            Identity(420)
        )

    def test_identity_functor_law_1(self):
        # fmap id = id
        x = Identity(42)
        left = x.fmap(identity)
        right = x
        self.assertEqual(left, right)

    def test_identity_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = Identity(42)

        left = x.fmap(compose(f, g))
        right = x.fmap(g).fmap(f)

        self.assertEquals(left, right)


class TestIdentityApplicative(unittest.TestCase):

    def test_identity_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        f = lambda x: x * 42
        x = Identity(42)

        left = Identity.pure(f).apply(x)
        right = x.fmap(f)

        self.assertEquals(left, right)

    def test_identity_applicative_law_identity(self):
        # pure id <*> v = v
        v = Identity(42)

        left = Identity.pure(identity).apply(v)
        right = v

        self.assertEquals(left, right)

    def test_identity_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u = Identity.pure(lambda x: x * 42)
        v = Identity.pure(lambda x: x + 42)
        w = Identity(42)

        left = Identity.pure(compose2).apply(u).apply(v).apply(w)
        right = u.apply(v.apply(w))

        self.assertEquals(left, right)

    def test_identity_applicative_law_homomorphism(self):
        # pure f <*> pure x = pure (f x)
        f = lambda x: x * 42
        x = 42

        left = Identity.pure(f).apply(Identity.pure(x))
        right = Identity.pure(f(42))
        self.assertEquals(left, right)

    def test_identity_applicative_law_interchange(self):
        # u <*> pure y = pure ($ y) <*> u

        y = 43
        u = Identity(lambda x: x*42)

        left = (u).apply(Identity.pure(y))
        right = Identity.pure(lambda f: f(y)).apply(u)

        self.assertEquals(left, right)


class TestIdentityMonad(unittest.TestCase):

    def test_identity_monad_bind(self):
        m = Identity(42)

        self.assertEqual(
            m.bind(lambda x: Identity(x*10)),
            Identity(420)
        )

    def test_identity_monad_law_left_identity(self):
        # return x >>= f is the same damn thing as f x

        f = lambda x: Identity(x+100000)
        x = Identity(3)

        self.assertEqual(
            x.bind(f),
            f(3)
        )

    def test_identity_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = Identity("move on up")

        self.assertEqual(
            m.bind(Identity.return_),
            m
        )

    def test_identity_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        f = lambda x: Identity(x+1000)
        g = lambda y: Identity(y*42)
        m = Identity(42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )

