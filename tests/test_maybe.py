import unittest
from collections.abc import Callable

from oslash.maybe import Just, Maybe, Nothing
from oslash.util import compose, fmap, identity


class TestMaybeFunctor(unittest.TestCase):
    def test_just_functor_map(self) -> None:
        f: Callable[[int], int] = lambda x: x * 2
        x: Maybe[int] = Just(21)

        assert x.map(f) == Just(42)

    def test_nothing_functor_map(self) -> None:
        f: Callable[[int], int] = lambda x: x + 2
        x: Maybe[int] = Nothing()

        assert x.map(f) == x

    def test_nothing_functor_law1(self) -> None:
        # fmap id = id
        assert Nothing().map(identity) == Nothing()

    def test_just_functor_law1(self) -> None:
        # fmap id = id
        x: Maybe[int] = Just(3)
        assert x.map(identity) == x

    def test_just_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        f: Callable[[int], int] = lambda x: x + 10
        g: Callable[[int], int] = lambda x: x * 10
        x: Maybe[int] = Just(42)

        assert x.map(compose(f, g)) == x.map(g).map(f)

    def test_nothing_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        f: Callable[[int], int] = lambda x: x + 10
        g: Callable[[int], int] = lambda x: x * 10
        x: Maybe[int] = Nothing()

        assert x.map(compose(f, g)) == x.map(g).map(f)


class TestMaybeApplicative(unittest.TestCase):
    def test_just_applicative_law_functor(self) -> None:
        # pure f <*> x = fmap f x
        x: Maybe[int] = Just.unit(42)
        f: Callable[[int], int] = lambda x: x * 42

        assert Just.pure(f).apply(x) == x.map(f)

    def test_nothing_applicative_law_functor(self) -> None:
        # pure f <*> x = fmap f x
        x: Maybe[int] = Nothing()
        f: Callable[[int], int] = lambda x: x * 42

        assert Just.pure(f).apply(x) == x.map(f)

    def test_just_applicative_law_identity(self) -> None:
        # pure id <*> v = v
        v: Maybe[int] = Just.unit(42)

        assert Just.pure(identity).apply(v) == v

    def test_nothing_applicative_law_identity(self) -> None:
        # pure id <*> v = v
        v: Maybe[int] = Nothing()

        assert Just.pure(identity).apply(v) == v

    def test_just_applicative_law_composition(self) -> None:
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w: Maybe[int] = Just.unit(42)
        mul_42: Callable[[int], int] = lambda x: x * 42
        add_42: Callable[[int], int] = lambda x: x + 42

        u = Just.pure(mul_42)
        v = Just.pure(add_42)

        assert Just.pure(fmap).apply(u).apply(v).apply(w) == u.apply(v.apply(w))

    def test_identity_applicative_law_composition(self) -> None:
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w: Maybe[int] = Nothing()
        mul_42: Callable[[int], int] = lambda x: x * 42
        add_42: Callable[[int], int] = lambda x: x + 42

        u = Just.pure(mul_42)
        v = Just.pure(add_42)

        assert Just.pure(fmap).apply(u).apply(v).apply(w) == u.apply(v.apply(w))

    def test_just_applicative_law_homomorphism(self) -> None:
        # pure f <*> pure x = pure (f x)
        x: int = 42
        f: Callable[[int], int] = lambda x: x * 42

        assert Just.pure(f).apply(Just.pure(x)) == Just.pure(f(x))

    def test_nothing_applicative_law_homomorphism(self) -> None:
        # pure f <*> pure x = pure (f x)
        f: Callable[[int], int] = lambda x: x * 42

        assert Just.pure(f).apply(Nothing()) == Nothing()

    def test_just_applicative_law_interchange(self) -> None:
        # u <*> pure y = pure ($ y) <*> u

        y: int = 43
        mul_42: Callable[[int], int] = lambda x: x * 42

        u: Maybe[int] = Just.unit(mul_42)

        assert u.apply(Just.pure(y)) == Just.pure(lambda f: f(y)).apply(u)

    def test_nothing_applicative_law_interchange(self) -> None:
        # u <*> pure y = pure ($ y) <*> u
        mul_42: Callable[[int], int] = lambda x: x * 42

        u: Maybe[int] = Just.unit(mul_42)

        assert u.apply(Nothing()) == Nothing().apply(u)

    def test_just_applicative_1(self) -> None:
        a = Just.pure(lambda x, y: x + y).apply(Just(2)).apply(Just(40))
        assert a != Nothing()
        assert a == Just(42)

    def test_just_applicative_2(self) -> None:
        a = Just.pure(lambda x, y: x + y).apply(Nothing()).apply(Just(42))
        assert a == Nothing()

    def test_just_applicative_3(self) -> None:
        a = Just.pure(lambda x, y: x + y).apply(Just(42)).apply(Nothing())
        assert a == Nothing()


class TestMaybeMonoid(unittest.TestCase):
    def test_maybe_monoid_nothing_append_just(self) -> None:
        m: Maybe[str] = Just("Python")

        assert Nothing() + m == m

    def test_maybe_monoid_just_append_nothing(self) -> None:
        m: Maybe[str] = Just("Python")

        assert m + Nothing() == m

    def test_maybe_monoid_just_append_just(self) -> None:
        m: Maybe[str] = Just("Python")
        n: Maybe[str] = Just(" rocks!")

        assert m + n == Just("Python rocks!")

    def test_maybe_monoid_concat(self) -> None:
        assert Maybe.concat([Just(2), Just(40), Just(42)]) == Just(84)


class TestMaybeMonad(unittest.TestCase):
    def test_just_monad_bind(self) -> None:
        m: Maybe[int] = Just.unit(42)
        f: Callable[[int], Maybe[int]] = lambda x: Just.unit(x * 10)

        assert m.bind(f) == Just.unit(420)

    def test_nothing_monad_bind(self) -> None:
        m: Maybe[int] = Nothing()
        f: Callable[[int], Maybe[int]] = lambda x: Just.unit(x * 10)

        assert m.bind(f) == Nothing()

    def test_just_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f: Callable[[int], Maybe[int]] = lambda x: Just.unit(x + 100000)
        x: int = 3

        assert Just.unit(x).bind(f) == f(x)

    def test_nothing_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f: Callable[[int], Maybe[int]] = lambda x: Just.unit(x + 100000)

        assert Nothing().bind(f) == Nothing()

    def test_just_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m: Maybe[str] = Just.unit("move on up")

        assert m.bind(Just.unit) == m

    def test_nothing_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m: Maybe[int] = Nothing()

        assert m.bind(Just.unit) == m

    def test_just_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m: Maybe[int] = Just.unit(42)
        f: Callable[[int], Maybe[int]] = lambda x: Just.unit(x + 1000)
        g: Callable[[int], Maybe[int]] = lambda y: Just.unit(y * 42)

        assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))

    def test_nothing_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m: Maybe[int] = Nothing()
        f: Callable[[int], Maybe[int]] = lambda x: Just.unit(x + 1000)
        g: Callable[[int], Maybe[int]] = lambda y: Just.unit(y * 42)

        assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))

    def test_combine_just_and_just_rule1(self) -> None:
        assert (Just(5) and Just(6)) == Just(6)

    def test_combine_just_and_just_rule2(self) -> None:
        assert (Just(0) and Just(6)) == Just(0)

    def test_combine_just_or_nothing_rule1(self) -> None:
        assert (Just(5) or Nothing()) == Just(5)

    def test_combine_just_or_nothing_rule2(self) -> None:
        assert (Just(0) or Nothing()) == Nothing()
