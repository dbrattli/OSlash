import unittest

from oslash.either import Right, Left


class TestEither(unittest.TestCase):

    def test_either_right_map(self) -> None:
        a = Right(42).map(lambda x: x * 10)
        self.assertEqual(a, Right(420))

    def test_either_left_map(self) -> None:
        a = Left(42).map(lambda x: x*10)
        self.assertEqual(a, Left(42))

    def test_either_right_functor_law1(self) -> None:
        """fmap id = id"""

        self.assertEqual(Right(3).map(lambda x: x), Right(3))

    def test_either_right_functor_law2(self) -> None:
        """fmap (f . g) x = fmap f (fmap g x)"""
        def f(x: int) -> int:
            return x + 10

        def g(x: int) -> int:
            return x * 10

        self.assertEqual(
            Right(42).map(f).map(g),
            Right(42).map(lambda x: g(f(x)))
        )

    def test_either_left_functor_law1(self) -> None:
        """fmap id = id"""

        self.assertEqual(Left(3).map(lambda x: x), Left(3))

    def test_either_left_functor_law2(self) -> None:
        """fmap (f . g) x = fmap f (fmap g x)"""
        def f(x):
            return x + 10

        def g(x):
            return x * 10

        self.assertEqual(
            Left(42).map(f).map(g),
            Left(42).map(lambda x: g(f(x)))
        )

    def test_right_applicative_1(self) -> None:
        a = Right.pure(lambda x, y: x + y).apply(Right(2)).apply(Right(40))
        self.assertNotEqual(a, Left(42))
        self.assertEqual(a, Right(42))

    def test_right_applicative_2(self) -> None:
        a = Right.pure(lambda x, y: x + y).apply(Left("error")).apply(Right(42))
        self.assertEqual(a, Left("error"))

    def test_right_applicative_3(self) -> None:
        a = Right.pure(lambda x, y: x + y).apply(Right(42)).apply(Left("error"))
        self.assertEqual(a, Left("error"))

    def test_either_monad_right_bind_right(self) -> None:
        m = Right(42).bind(lambda x: Right(x * 10))
        self.assertEqual(m, Right(420))

    def test_either_monad_right_bind_left(self) -> None:
        """Nothing >>= \\x -> return (x*10)"""
        m = Left("error").bind(lambda x: Right(x * 10))
        self.assertEqual(m, Left("error"))
