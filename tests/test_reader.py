import unittest

from oslash import Reader
from oslash.reader import MonadReader
from oslash.util import identity, compose, fmap

pure = Reader.pure
unit = Reader.unit
asks = MonadReader.asks


class TestReader(unittest.TestCase):

    def test_reader_run(self):
        r = Reader(lambda name: "Hello, %s!" % name)
        greeting = r.run()("adit")
        self.assertEqual(greeting, "Hello, adit!")

    def test_reader_asks(self):
        a = asks(len).run()("Banana")
        self.assertEqual(6, a)


class TestReaderFunctor(unittest.TestCase):

    def test_reader_functor_map(self):
        x = unit(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.map(f),
            unit(420)
        )

    def test_reader_functor_law_1(self):
        # fmap id = id
        x = unit(42)

        self.assertEqual(
            x.map(identity),
            x
        )

    def test_reader_functor_law2(self):
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


class TestReaderApplicative(unittest.TestCase):

    def test_reader_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        x = unit(42)
        f = lambda e: e * 42

        self.assertEquals(
            pure(f).apply(x),
            x.map(f)
        )

    def test_reader_applicative_law_identity(self):
        # pure id <*> v = v
        v = unit(42)

        self.assertEquals(
            pure(identity).apply(v),
            v
        )

    def test_reader_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = unit(42)
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEquals(
            pure(fmap).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_reader_applicative_law_homomorphism(self):
        # pure f <*> pure x = pure (f x)
        x = 42
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(unit(x)),
            unit(f(x))
        )

    def test_reader_applicative_law_interchange(self):
        # u <*> pure y = pure ($ y) <*> u

        y = 43
        u = pure(lambda x: x*42)

        self.assertEquals(
            u.apply(unit(y)),
            pure(lambda f: f(y)).apply(u)
        )


class TestReaderMonad(unittest.TestCase):

    def test_reader_monad_bind(self):
        m = unit(42)
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            unit(420)
        )

    def test_reader_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x+100000)
        x = 3

        self.assertEqual(
            unit(x).bind(f),
            f(x)
        )

    def test_reader_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = unit("move on up")

        self.assertEqual(
            m.bind(unit),
            m
        )

    def test_reader_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = unit(42)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )
