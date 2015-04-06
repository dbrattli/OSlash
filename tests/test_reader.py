import unittest

from oslash import Reader
from oslash.util import identity, compose, compose2

pure = Reader.pure
return_ = Reader.return_


class TestReader(unittest.TestCase):

    def test_reader_run_reader(self):
        r = Reader(lambda name: "Hello, %s!" % name)
        greeting = r.run_reader()("adit")
        self.assertEqual(greeting, "Hello, adit!")


class TestReaderFunctor(unittest.TestCase):

    def test_reader_functor_fmap(self):
        x = return_(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.fmap(f),
            return_(420)
        )

    def test_reader_functor_law_1(self):
        # fmap id = id
        x = return_(42)

        self.assertEqual(
            x.fmap(identity),
            x
        )

    def test_reader_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = return_(42)

        self.assertEquals(
            x.fmap(compose(f, g)),
            x.fmap(g).fmap(f)
        )


class TestReaderApplicative(unittest.TestCase):

    def test_identity_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        x = return_(42)
        f = lambda e: e * 42

        self.assertEquals(
            pure(f).apply(x),
            x.fmap(f)
        )

    def test_identity_applicative_law_identity(self):
        # pure id <*> v = v
        v = return_(42)

        self.assertEquals(
            pure(identity).apply(v),
            v
        )

    def test_identity_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = return_(42)
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEquals(
            pure(compose2).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_identity_applicative_law_homomorphism(self):
        # pure f <*> pure x = pure (f x)
        x = 42
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(return_(x)),
            return_(f(x))
        )

    def test_identity_applicative_law_interchange(self):
        # u <*> pure y = pure ($ y) <*> u

        y = 43
        u = pure(lambda x: x*42)

        self.assertEquals(
            u.apply(return_(y)),
            pure(lambda f: f(y)).apply(u)
        )


# class TestReaderMonad(unittest.TestCase):
#     def test_reader_return(self):
#         v = 45
#         r = Reader.return_(v)
#         self.assertEqual(
#             r(42),
#             v
#         )

#     def test_reader_monad_bind(self):
#         v = 62
#         m = Reader.return_(v).bind(lambda x: Reader(lambda y: y+x))
#         self.assertEqual(
#             m(10),
#             v+10
#         )
