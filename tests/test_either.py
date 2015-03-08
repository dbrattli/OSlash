import unittest

from ø.either import Right, Left


class TestEither(unittest.TestCase):
    def test_either_right_fmap(self):
        a = Right(42).fmap(lambda x: x*10)
        self.assertEqual(a, Right(420))

    def test_either_left_fmap(self):
        a = Left(42).fmap(lambda x: x*10)
        self.assertEqual(a, Left(42))

    def test_either_right_functor_law1(self):
        """fmap id = id"""
        _id = lambda x: x
        self.assertEquals(Right(3).fmap(_id), Right(3))

    def test_either_right_functor_law2(self):
        """fmap (f . g) x = fmap f (fmap g x)"""
        def f(x):
            return x+10

        def g(x):
            return x*10

        self.assertEquals(
            Right(42).fmap(f).fmap(g),
            Right(42).fmap(lambda x: g(f(x)))
        )

    def test_either_left_functor_law1(self):
        """fmap id = id"""
        _id = lambda x: x
        self.assertEquals(Left(3).fmap(_id), Left(3))

    def test_either_left_functor_law2(self):
        """fmap (f . g) x = fmap f (fmap g x)"""
        def f(x):
            return x+10

        def g(x):
            return x*10

        self.assertEquals(
            Left(42).fmap(f).fmap(g),
            Left(42).fmap(lambda x: g(f(x)))
        )
