"""
Tests for the Identity Monad.

Functor laws:
    * http://learnyouahaskell.com/functors-applicative-functors-and-monoids

Applicative laws:
    * http://en.wikibooks.org/wiki/Haskell/Applicative_Functors

Monad laws:
    * http://learnyouahaskell.com/a-fistful-of-monads#monad-laws
    * https://wiki.haskell.org/Monad_laws
"""

import unittest
from collections.abc import Callable

from oslash.identity import Identity
from oslash.util import compose, fmap, identity


class TestIdentityFunctor(unittest.TestCase):
    def test_identity_functor_map(self) -> None:
        x = Identity.unit(42)
        f: Callable[[int], int] = lambda x: x * 10

        assert x.map(f) == Identity.unit(420)

    def test_identity_functor_law_1(self) -> None:
        # fmap id = id
        x = Identity.unit(42)

        assert x.map(identity) == x

    def test_identity_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x: int) -> int:
            return x + 10

        def g(x: int) -> int:
            return x * 10

        x = Identity.unit(42)

        assert x.map(compose(f, g)) == x.map(g).map(f)


class TestIdentityApplicative(unittest.TestCase):
    def test_identity_applicative_law_functor(self) -> None:
        # pure f <*> x = fmap f x
        x = Identity.unit(42)
        f: Callable[[int], int] = lambda x: x * 42

        assert Identity.pure(f).apply(x) == x.map(f)

    def test_identity_applicative_law_identity(self) -> None:
        # pure id <*> v = v
        v = Identity.unit(42)

        assert Identity.pure(identity).apply(v) == v

    def test_identity_applicative_law_composition(self) -> None:
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = Identity.unit(42)
        u: Identity[Callable[[int], int]] = Identity.pure(lambda x: x * 42)
        v: Identity[Callable[[int], int]] = Identity.pure(lambda x: x + 42)

        assert Identity.pure(fmap).apply(u).apply(v).apply(w) == u.apply(v.apply(w))

    def test_identity_applicative_law_homomorphism(self) -> None:
        # pure f <*> pure x = pure (f x)
        x: int = 42
        f: Callable[[int], int] = lambda x: x * 42

        assert Identity.pure(f).apply(Identity.pure(x)) == Identity.pure(f(x))

    def test_identity_applicative_law_interchange(self) -> None:
        # u <*> pure y = pure ($ y) <*> u

        y: int = 43
        u: Identity[Callable[[int], int]] = Identity.unit(lambda x: x * 42)
        dollar_y: Callable[[Callable[[int], int]], int] = lambda f: f(y)

        assert u.apply(Identity.pure(y)) == Identity.pure(dollar_y).apply(u)


class TestIdentityMonad(unittest.TestCase):
    def test_identity_monad_bind(self) -> None:
        m = Identity.unit(42)
        f: Callable[[int], Identity[int]] = lambda x: Identity.unit(x * 10)

        assert m.bind(f) == Identity.unit(420)

    def test_identity_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f: Callable[[int], Identity[int]] = lambda x: Identity.unit(x + 100000)
        x: int = 3

        assert Identity.unit(x).bind(f) == f(x)

    def test_identity_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m = Identity.unit("move on up")

        assert m.bind(Identity.unit) == m

    def test_identity_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = Identity.unit(42)
        f: Callable[[int], Identity[int]] = lambda x: Identity.unit(x + 1000)
        g: Callable[[int], Identity[int]] = lambda y: Identity.unit(y * 42)

        assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))
