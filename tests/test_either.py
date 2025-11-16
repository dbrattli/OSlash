import unittest
from collections.abc import Callable

from oslash.either import Either, Left, Right


class TestEither(unittest.TestCase):
    def test_either_right_map(self) -> None:
        f: Callable[[int], int] = lambda x: x * 10
        a: Either[int, int] = Right(42).map(f)
        assert a == Right(420)

    def test_either_left_map(self) -> None:
        f: Callable[[int], int] = lambda x: x * 10
        a: Either[int, int] = Left(42).map(f)
        assert a == Left(42)

    def test_either_right_functor_law1(self) -> None:
        """fmap id = id"""
        identity: Callable[[int], int] = lambda x: x

        assert Right(3).map(identity) == Right(3)

    def test_either_right_functor_law2(self) -> None:
        """fmap (f . g) x = fmap f (fmap g x)"""
        f: Callable[[int], int] = lambda x: x + 10
        g: Callable[[int], int] = lambda x: x * 10

        assert Right(42).map(f).map(g) == Right(42).map(lambda x: g(f(x)))

    def test_either_left_functor_law1(self) -> None:
        """fmap id = id"""
        identity: Callable[[int], int] = lambda x: x

        assert Left(3).map(identity) == Left(3)

    def test_either_left_functor_law2(self) -> None:
        """fmap (f . g) x = fmap f (fmap g x)"""
        f: Callable[[int], int] = lambda x: x + 10
        g: Callable[[int], int] = lambda x: x * 10

        assert Left(42).map(f).map(g) == Left(42).map(lambda x: g(f(x)))

    def test_right_applicative_1(self) -> None:
        a: Either[int, int] = Right.pure(lambda x, y: x + y).apply(Right(2)).apply(Right(40))
        assert a != Left(42)
        assert a == Right(42)

    def test_right_applicative_2(self) -> None:
        a: Either[str, int] = Right.pure(lambda x, y: x + y).apply(Left("error")).apply(Right(42))
        assert a == Left("error")

    def test_right_applicative_3(self) -> None:
        a: Either[str, int] = Right.pure(lambda x, y: x + y).apply(Right(42)).apply(Left("error"))
        assert a == Left("error")

    def test_either_monad_right_bind_right(self) -> None:
        f: Callable[[int], Either[str, int]] = lambda x: Right(x * 10)
        m: Either[str, int] = Right(42).bind(f)
        assert m == Right(420)

    def test_either_monad_right_bind_left(self) -> None:
        """Nothing >>= \\x -> return (x*10)"""
        f: Callable[[int], Either[str, int]] = lambda x: Right(x * 10)
        m: Either[str, int] = Left("error").bind(f)
        assert m == Left("error")
