import unittest
from collections.abc import Callable

from oslash.util import compose, identity


class TestCompose(unittest.TestCase):
    def test_identity(self) -> None:
        assert identity(42) == 42

    def test_compose_0(self) -> None:
        f_id = compose()
        assert f_id(42) == 42

    def test_compose_1(self) -> None:
        f: Callable[[int], int] = lambda x: x * 42
        g = compose(f)
        assert g(10) == 420

    def test_compose_2(self) -> None:
        f: Callable[[int], int] = lambda x: x * 42
        g: Callable[[int], int] = lambda y: y + 10
        h = compose(g, f)
        assert h(10) == 430

    def test_compose_3(self) -> None:
        f: Callable[[int], int] = lambda x: x * 42
        g: Callable[[int], int] = lambda y: y + 10
        h: Callable[[int], float] = lambda z: z / 2
        i = compose(h, g, f)
        assert i(10) == 215

    def test_compose_composition(self) -> None:
        u: Callable[[int], int] = lambda x: x * 42
        v: Callable[[int], int] = lambda x: x + 42
        w: int = 42

        a = compose(u, v)(w)
        b = u(v(w))
        assert a == b
