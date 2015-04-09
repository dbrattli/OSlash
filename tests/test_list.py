# coding=utf-8
import unittest

from oslash.list import List
from oslash.util import identity, compose, compose2, Unit

pure = List.pure
unit = List.unit


class TestListFunctor(unittest.TestCase):

    def test_list_functor_fmap(self):
        # fmap f (return v) = return (f v)
        x = unit(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.fmap(f),
            unit(420)
        )

        y = List([1, 2, 3, 4])
        g = lambda x: x * 10

        self.assertEqual(
            y.fmap(g),
            List([10, 20, 30, 40])
        )

    def test_list_functor_law_1(self):
        # fmap id = id

        # Singleton list using return
        x = unit(42)
        self.assertEqual(
            x.fmap(identity),
            x
        )

        # Empty list
        y = List()
        self.assertEqual(
            y.fmap(identity),
            y
        )

        # Long list
        z = List(range(42))
        self.assertEqual(
            z.fmap(identity),
            z
        )

    def test_list_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        # Singleton list
        x = unit(42)
        self.assertEquals(
            x.fmap(compose(f, g)),
            x.fmap(g).fmap(f)
        )

        # Empty list
        y = List([])
        self.assertEquals(
            y.fmap(compose(f, g)),
            y.fmap(g).fmap(f)
        )

        # Long list
        z = List(range(42))
        self.assertEquals(
            z.fmap(compose(f, g)),
            z.fmap(g).fmap(f)
        )


class TestListApplicative(unittest.TestCase):

    def test_list_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        f = lambda x: x * 42

        x = unit(42)
        self.assertEquals(
            pure(f).apply(x),
            x.fmap(f)
        )

        # Empty list
        z = List()
        self.assertEquals(
            pure(f).apply(z),
            z.fmap(f)
        )

        # Long list
        z = List(range(42))
        self.assertEquals(
            pure(f).apply(z),
            z.fmap(f)
        )

    def test_list_applicative_law_identity(self):
        # pure id <*> v = v

        # Singleton list
        x = unit(42)
        self.assertEquals(
            pure(identity).apply(x),
            x
        )

        # Empty list
        y = List([])
        self.assertEquals(
            pure(identity).apply(y),
            y
        )

        # Log list
        y = List(range(42))
        self.assertEquals(
            pure(identity).apply(y),
            y
        )

    def test_identity_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        # Singleton list
        w = unit(42)
        self.assertEquals(
            pure(compose2).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_identity_applicative_law_composition_empty(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        # Empty list
        w = List()
        self.assertEquals(
            pure(compose2).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_identity_applicative_law_composition_range(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        # Long list
        w = List(range(42))
        self.assertEquals(
            pure(compose2).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_list_applicative_binary_func_singleton(self):
        f = lambda x, y: x+y
        v = unit(2)
        w = unit(40)

        self.assertEquals(
            pure(f).apply(v).apply(w),
            unit(42)
        )

    def test_list_applicative_unary_func(self):
        f = lambda x: x * 2
        v = unit(21)

        self.assertEquals(
            pure(f).apply(v),
            unit(42)
        )

    def test_list_applicative_binary_func(self):
        f = lambda x, y: x+y
        v = List([1, 2])
        w = List([4, 8])

        self.assertEquals(
            pure(f).apply(v).apply(w),
            List([5, 9, 6, 10])
        )

    def test_list_applicative_empty_func(self):
        f = []
        v = unit(42)
        w = List([1, 2, 3])

        self.assertEquals(
            List(f).apply(v).apply(w),
            List(Unit)
        )

    def test_list_applicative_binary_func_empty_arg_1(self):
        f = lambda x, y: x+y
        v = unit(42)
        e = List()

        self.assertEquals(
            pure(f).apply(e).apply(v),
            List()
        )

    def test_list_applicative_binary_func_empty_arg_2(self):
        f = lambda x, y: x+y
        v = unit(42)
        e = List()

        self.assertEquals(
            pure(f).apply(v).apply(e),
            List()
        )


class TestListMonad(unittest.TestCase):

    def test_list_monad_bind(self):
        m = unit(42)
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            unit(420)
        )

    def test_list_monad_empty_bind(self):
        m = List()
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            List()
        )

    def test_list_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x+100000)
        v = 42

        self.assertEqual(
            unit(v).bind(f),
            f(v)
        )

    def test_list_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = unit("move on up")

        self.assertEqual(
            m.bind(unit),
            m
        )

    def test_list_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        m = unit(42)
        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )

    def test_list_monad_law_associativity_empty(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        # Empty list
        m = List()
        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )

    def test_list_monad_law_associativity_range(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        # Long list
        m = List(range(42))
        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )
