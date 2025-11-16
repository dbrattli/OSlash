import unittest
from collections.abc import Callable

from oslash import Reader
from oslash.reader import MonadReader
from oslash.util import compose, fmap, identity

env = 42


class TestReader(unittest.TestCase):
    def test_reader_run(self) -> None:
        r: Reader[str, str] = Reader(lambda name: f"Hello, {name}!")
        greeting: str = r.run("adit")
        assert greeting == "Hello, adit!"

    def test_reader_asks(self) -> None:
        a: int = MonadReader.asks(len).run("Banana")
        assert a == 6


class TestReaderFunctor(unittest.TestCase):
    def test_reader_functor_map(self) -> None:
        x: Reader[int, int] = Reader.unit(42)
        f: Callable[[int], int] = lambda x: x * 10

        assert x.map(f).run(env) == Reader.unit(420).run(env)

    def test_reader_functor_law_1(self) -> None:
        # fmap id = id
        x: Reader[int, int] = Reader.unit(42)

        assert x.map(identity).run(env) == x.run(env)

    def test_reader_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        f: Callable[[int], int] = lambda x: x + 10
        g: Callable[[int], int] = lambda x: x * 10

        x: Reader[int, int] = Reader.unit(42)

        assert x.map(compose(f, g)).run(env) == x.map(g).map(f).run(env)


class TestReaderApplicative(unittest.TestCase):
    def test_reader_applicative_law_functor(self) -> None:
        # pure f <*> x = fmap f x
        x: Reader[int, int] = Reader.unit(42)
        f: Callable[[int], int] = lambda e: e * 42

        assert Reader.pure(f).apply(x).run(env) == x.map(f).run(env)

    def test_reader_applicative_law_identity(self) -> None:
        # pure id <*> v = v
        v: Reader[int, int] = Reader.unit(42)

        assert Reader.pure(identity).apply(v).run(env) == v.run(env)

    def test_reader_applicative_law_composition(self) -> None:
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w: Reader[int, int] = Reader.unit(42)
        mul_42: Callable[[int], int] = lambda x: x * 42
        add_42: Callable[[int], int] = lambda x: x + 42
        u: Reader[int, Callable[[int], int]] = Reader.pure(mul_42)
        v: Reader[int, Callable[[int], int]] = Reader.pure(add_42)

        assert Reader.pure(fmap).apply(u).apply(v).apply(w).run(env) == u.apply(v.apply(w)).run(env)

    def test_reader_applicative_law_homomorphism(self) -> None:
        # pure f <*> pure x = pure (f x)
        x: int = 42
        f: Callable[[int], int] = lambda x: x * 42

        assert Reader.pure(f).apply(Reader.unit(x)).run(env) == Reader.unit(f(x)).run(env)

    def test_reader_applicative_law_interchange(self) -> None:
        # u <*> pure y = pure ($ y) <*> u

        y: int = 43
        mul_42: Callable[[int], int] = lambda x: x * 42
        u: Reader[int, Callable[[int], int]] = Reader.pure(mul_42)

        assert u.apply(Reader.unit(y)).run(env) == Reader.pure(lambda f: f(y)).apply(u).run(env)


class TestReaderMonad(unittest.TestCase):
    def test_reader_monad_bind(self) -> None:
        m: Reader[int, int] = Reader.unit(42)
        f: Callable[[int], Reader[int, int]] = lambda x: Reader.unit(x * 10)

        assert m.bind(f).run(env) == Reader.unit(420).run(env)

    def test_reader_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f: Callable[[int], Reader[int, int]] = lambda x: Reader.unit(x + 100000)
        x: int = 3

        assert Reader.unit(x).bind(f).run(env) == f(x).run(env)

    def test_reader_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m: Reader[int, str] = Reader.unit("move on up")

        assert m.bind(Reader.unit).run(env) == m.run(env)

    def test_reader_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m: Reader[int, int] = Reader.unit(42)
        f: Callable[[int], Reader[int, int]] = lambda x: Reader.unit(x + 1000)
        g: Callable[[int], Reader[int, int]] = lambda y: Reader.unit(y * 42)

        assert m.bind(f).bind(g).run(env) == m.bind(lambda x: f(x).bind(g)).run(env)
