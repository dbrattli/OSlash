#!/usr/bin/env python3
import unittest

from oslash.do import do, guard, let  # type: ignore[attr-defined]
from oslash.list import List


class TestDo(unittest.TestCase):
    def test_do_list_basic(self) -> None:
        l = lambda *items: List.from_iterable(items)  # type: ignore[misc]
        out1 = do(let(a=l(3, 10, 6)), let(b=l(100, 200)), lambda e: List.unit(e.a + e.b))  # type: ignore[misc]
        out2 = l(3, 10, 6) | (lambda a: l(100, 200) | (lambda b: List.unit(a + b)))  # type: ignore[misc]
        assert out1 == out2

    def test_do_list_pythag(self) -> None:
        r = lambda low, high: List.from_iterable(range(low, high))  # type: ignore[misc]
        out1 = do(
            let(z=r(1, 21)),
            let(x=lambda e: r(1, e.z + 1)),  # type: ignore[misc]
            let(y=lambda e: r(e.x, e.z + 1)),  # type: ignore[misc]
            lambda e: guard(List, e.x * e.x + e.y * e.y == e.z * e.z),  # type: ignore[misc]
            lambda e: List.unit((e.x, e.y, e.z)),  # type: ignore[misc]
        )  # type: ignore[misc]
        out2 = r(1, 21) | (  # type: ignore[operator]
            lambda z: r(1, z + 1)  # type: ignore[misc]
            | (lambda x: r(x, z + 1) | (lambda y: guard(List, x * x + y * y == z * z) >> List.unit((x, y, z))))  # type: ignore[misc]
        )  # type: ignore[misc]
        assert out1 == out2

    # TODO: add more tests


class TestDoErrors(unittest.TestCase):
    def test_do_invalid_input(self) -> None:
        try:
            do("some invalid input")  # type: ignore[arg-type]
        except TypeError:
            pass
        else:
            raise AssertionError

    def test_do_scoping_correct(self) -> None:
        try:
            l = lambda *items: List.from_iterable(items)  # type: ignore[misc]
            do(let(a=l(1, 2, 3)), let(b=lambda e: List.unit(e.a)), lambda e: List.unit(e.a * e.b))  # type: ignore[misc]
        except AttributeError:
            raise AssertionError

    def test_do_scoping_invalid(self) -> None:
        try:
            l = lambda *items: List.from_iterable(items)  # type: ignore[misc]
            do(let(a=lambda e: List.unit(e.b)), let(b=l(1, 2, 3)), lambda e: List.unit(e.a * e.b))  # type: ignore[misc]
        except AttributeError:
            pass
        else:
            raise AssertionError
