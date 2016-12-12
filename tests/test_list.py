# coding=utf-8
import unittest

from oslash.list import List
from oslash.util import identity, compose, fmap, Unit

pure = List.pure
unit = List.unit


class TestList(unittest.TestCase):
    def test_list_null(self):
        xs = List()
        assert(xs.null())

    def test_list_not_null_after_cons_and_tail(self):
        xs = List().cons(1).tail()
        assert(xs.null())

    def test_list_not_null_after_cons(self):
        xs = List().cons(1)
        assert(not xs.null())

    def test_list_head(self):
        x = List().cons(42).head()
        self.assertEqual(42, x)

    def test_list_tail_head(self):
        xs = List().cons("b").cons("a")
        self.assertEqual("a", xs.head())

    def test_list_tail_tail_null(self):
        xs = List().cons("b").cons("a")
        assert(xs.tail().tail().null())

    def test_list_list(self):
        xs = List().cons(List().cons(42))
        self.assertEqual(42, xs.head().head())

    def test_list_length_empty(self):
        xs = List()
        self.assertEqual(0, len(xs))

    def test_list_length_non_empty(self):
        xs = List.unit(42)
        self.assertEqual(1, len(xs))

    def test_list_length_multiple(self):
        xs = List.from_iterable(range(42))
        self.assertEqual(42, len(xs))

    def test_list_append_empty(self):
        xs = List()
        ys = List.unit(42)
        zs = xs.append(ys)
        self.assertEqual(ys, zs)

    def test_list_append_empty_other(self):
        xs = List.unit(42)
        ys = List()
        zs = xs.append(ys)
        self.assertEqual(xs, zs)

    def test_list_append_non_empty(self):
        xs = List.from_iterable(range(5))
        ys = List.from_iterable(range(5, 10))
        zs = xs.append(ys)
        self.assertEqual(List.from_iterable(range(10)), zs)


class TestListFunctor(unittest.TestCase):

    def test_list_functor_map(self):
        # fmap f (return v) = return (f v)
        x = unit(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.map(f),
            unit(420)
        )

        y = List.from_iterable([1, 2, 3, 4])
        g = lambda x: x * 10

        self.assertEqual(
            y.map(g),
            List.from_iterable([10, 20, 30, 40])
        )

    def test_list_functor_law_1(self):
        # fmap id = id

        # Singleton list using return
        x = unit(42)
        self.assertEqual(
            x.map(identity),
            x
        )

        # Empty list
        y = List()
        self.assertEqual(
            y.map(identity),
            y
        )

        # Long list
        z = List.from_iterable(range(42))
        self.assertEqual(
            z.map(identity),
            z
        )

    def test_list_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x + 10

        def g(x):
            return x * 10

        # Singleton list
        x = unit(42)
        self.assertEquals(
            x.map(compose(f, g)),
            x.map(g).map(f)
        )

        # Empty list
        y = List.empty()
        self.assertEquals(
            y.map(compose(f, g)),
            y.map(g).map(f)
        )

        # Long list
        z = List.from_iterable(range(42))
        self.assertEquals(
            z.map(compose(f, g)),
            z.map(g).map(f)
        )


class TestListApplicative(unittest.TestCase):

    def test_list_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        f = lambda x: x * 42

        x = unit(42)
        self.assertEquals(
            pure(f).apply(x),
            x.map(f)
        )

        # Empty list
        z = List()
        self.assertEquals(
            pure(f).apply(z),
            z.map(f)
        )

        # Long list
        z = List.from_iterable(range(42))
        self.assertEquals(
            pure(f).apply(z),
            z.map(f)
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
        y = List.empty()
        self.assertEquals(
            pure(identity).apply(y),
            y
        )

        # Log list
        y = List.from_iterable(range(42))
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
            pure(fmap).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_identity_applicative_law_composition_empty(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        # Empty list
        w = List()
        self.assertEquals(
            pure(fmap).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_identity_applicative_law_composition_range(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        # Long list
        w = List.from_iterable(range(42))
        self.assertEquals(
            pure(fmap).apply(u).apply(v).apply(w),
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
        v = List.from_iterable([1, 2])
        w = List.from_iterable([4, 8])

        self.assertEquals(
            pure(f).apply(v).apply(w),
            List.from_iterable([5, 9, 6, 10])
        )

    def test_list_applicative_empty_func(self):
        v = unit(42)
        w = List.from_iterable([1, 2, 3])

        self.assertEquals(
            List.empty().apply(v).apply(w),
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
        m = List.from_iterable(range(42))
        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )
