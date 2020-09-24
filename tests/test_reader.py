import unittest

from oslash import Reader
from oslash.reader import MonadReader
from oslash.util import identity, compose, fmap

pure = Reader.pure
unit = Reader.unit
asks = MonadReader.asks


env = 42

class TestReader(unittest.TestCase):

    def test_reader_run(self) -> None:
        r = Reader(lambda name: "Hello, %s!" % name)
        greeting = r.run("adit")
        self.assertEqual(greeting, "Hello, adit!")

    def test_reader_asks(self) -> None:
        a = asks(len).run("Banana")
        self.assertEqual(6, a)


class TestReaderFunctor(unittest.TestCase):

    def test_reader_functor_map(self) -> None:
        x = unit(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.map(f).run(env),
            unit(420).run(env)
        )

    def test_reader_functor_law_1(self) -> None:
        # fmap id = id
        x = unit(42)

        self.assertEqual(
            x.map(identity).run(env),
            x.run(env)
        )

    def test_reader_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = unit(42)

        self.assertEqual(
            x.map(compose(f, g)).run(env),
            x.map(g).map(f).run(env)
        )


class TestReaderApplicative(unittest.TestCase):

    def test_reader_applicative_law_functor(self) -> None:
        # pure f <*> x = fmap f x
        x = unit(42)
        f = lambda e: e * 42

        self.assertEqual(
            pure(f).apply(x).run(env),
            x.map(f).run(env)
        )

    def test_reader_applicative_law_identity(self) -> None:
        # pure id <*> v = v
        v = unit(42)

        self.assertEqual(
            pure(identity).apply(v).run(env),
            v.run(env)
        )

    def test_reader_applicative_law_composition(self) -> None:
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = unit(42)
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEqual(
            pure(fmap).apply(u).apply(v).apply(w).run(env),
            u.apply(v.apply(w)).run(env)
        )

    def test_reader_applicative_law_homomorphism(self) -> None:
        # pure f <*> pure x = pure (f x)
        x = 42
        f = lambda x: x * 42

        self.assertEqual(
            pure(f).apply(unit(x)).run(env),
            unit(f(x)).run(env)
        )

    def test_reader_applicative_law_interchange(self) -> None:
        # u <*> pure y = pure ($ y) <*> u

        y = 43
        u = pure(lambda x: x*42)

        self.assertEqual(
            u.apply(unit(y)).run(env),
            pure(lambda f: f(y)).apply(u).run(env)
        )


class TestReaderMonad(unittest.TestCase):

    def test_reader_monad_bind(self) -> None:
        m = unit(42)
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f).run(env),
            unit(420).run(env)
        )

    def test_reader_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x+100000)
        x = 3

        self.assertEqual(
            unit(x).bind(f).run(env),
            f(x).run(env)
        )

    def test_reader_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m = unit("move on up")

        self.assertEqual(
            m.bind(unit).run(env),
            m.run(env)
        )

    def test_reader_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = unit(42)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        self.assertEqual(
            m.bind(f).bind(g).run(env),
            m.bind(lambda x: f(x).bind(g)).run(env)
        )
