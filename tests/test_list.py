# coding=utf-8
import unittest

from oslash.list import List
from oslash.util import identity, compose, compose2

pure = List.pure
return_ = List.return_


class TestListFunctor(unittest.TestCase):

    def test_list_functor_fmap(self):
        # fmap f (return v) = return (f v)
        x = return_([1, 2, 3, 4])
        f = lambda x: x * 10

        self.assertEqual(
            x.fmap(f),
            return_([10, 20, 30, 40])
        )

    def test_list_functor_law_1(self):
        # fmap id = id
        x = return_([range(1, 42)])

        self.assertEqual(
            x.fmap(identity),
            x
        )

        y = return_([])

        self.assertEqual(
            y.fmap(identity),
            y
        )

    def test_list_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = return_([1, 2, 3])

        self.assertEquals(
            x.fmap(compose(f, g)),
            x.fmap(g).fmap(f)
        )


class TestListApplicative(unittest.TestCase):

    def test_list_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        x = return_(range(42))
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(x),
            x.fmap(f)
        )

    def test_list_applicative_law_identity(self):
        # pure id <*> v = v
        v = return_(range(42))

        self.assertEquals(
            pure(identity).apply(v),
            v
        )

    def test_identity_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = return_(range(42))
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEquals(
            pure(compose2).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_list_applicative_binary_func_singleton(self):
        f = lambda x, y: x+y
        v = return_(2)
        w = return_(40)

        self.assertEquals(
            pure(f).apply(v).apply(w),
            return_(42)
        )

    def test_list_applicative_unary_func(self):
        f = lambda x: x * 2
        v = return_([1, 2])

        self.assertEquals(
            pure(f).apply(v),
            return_([2, 4])
        )

    def test_list_applicative_binary_func(self):
        f = lambda x, y: x+y
        v = return_([1, 2])
        w = return_([4, 8])

        self.assertEquals(
            pure(f).apply(v).apply(w),
            return_([5, 9, 6, 10])
        )

    def test_list_applicative_empty_func(self):
        f = []
        v = return_(42)
        w = return_([1, 2, 3])
        a = pure(f).apply(v).apply(w)

        self.assertEquals(
            a,
            return_([])
        )

    def test_list_applicative_binary_func_empty_arg_1(self):
        f = lambda x, y: x+y
        v = return_(42)
        e = return_([])
        a = pure(f).apply(e).apply(v)

        self.assertEquals(
            a,
            return_([])
        )

    def test_list_applicative_binary_func_empty_arg_2(self):
        f = lambda x, y: x+y
        v = return_(42)
        e = return_([])

        self.assertEquals(
            pure(f).apply(v).apply(e),
            return_([])
        )


class TestListMonad(unittest.TestCase):

    def test_list_monad_bind(self):
        m = return_([42])
        f = lambda x: return_(x*10)

        self.assertEqual(
            m.bind(f),
            return_([420])
        )

    def test_list_monad_empty_bind(self):
        m = return_([])
        f = lambda x: return_(x*10)

        self.assertEqual(
            m.bind(f),
            return_([])
        )

    def test_list_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: return_(x+100000)
        x = 42

        self.assertEqual(
            return_(x).bind(f),
            f(x)
        )

    def test_list_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = return_("move on up")

        self.assertEqual(
            m.bind(return_),
            m
        )

    def test_list_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = return_(42)
        f = lambda x: return_(x+1000)
        g = lambda y: return_(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )
