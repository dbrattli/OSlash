import unittest
from collections.abc import Callable

from oslash.cont import Cont
from oslash.util import compose, identity


class TestCont(unittest.TestCase):
    def test_cont_pythagoras(self) -> None:
        add: Callable[[int], Callable[[int], Cont[int, int]]] = lambda x: lambda y: Cont.unit(x + y)
        square: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x * x)

        pythagoras = lambda x: lambda y: square(x) | (lambda xx: (square(y) | (lambda yy: add(xx)(yy))))

        assert pythagoras(4)(4)(identity) == 32

    def test_cont_basic(self) -> None:
        add: Callable[[int, int], int] = lambda x, y: x + y
        add_cont: Cont[int, Callable[[int, int], int]] = Cont.unit(add)

        assert add_cont(identity)(40, 2) == 42

    def test_cont_simple(self) -> None:
        f: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x * 3)
        g: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x - 2)
        h: Callable[[int], Cont[int, int]] = lambda x: f(x) if x == 5 else g(x)

        do_c: Cont[int, str] = Cont.unit(5) | h
        final_c: Callable[[int], str] = lambda x: f"Done: {x}"

        assert do_c.run(final_c) == "Done: 15"

    def test_cont_simpler(self) -> None:
        f: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x * 3)
        g: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x - 2)
        h: Callable[[int], Cont[int, int]] = lambda x: f(x) if x == 5 else g(x)

        do_c: Cont[int, str] = Cont.unit(4) | h
        final_c: Callable[[int], str] = lambda x: f"Done: {x}"

        assert do_c.run(final_c) == "Done: 2"

    def test_cont_call_cc(self) -> None:
        f: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x * 3)
        g: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x - 2)
        h = lambda x, abort: f(x) if x == 5 else abort(-1)

        do_c = lambda n: Cont.unit(n) | (lambda x: Cont.call_cc(lambda abort: h(x, abort))) | (lambda y: g(y))
        final_c: Callable[[int], str] = lambda x: f"Done: {x}"

        assert do_c(5).run(final_c) == "Done: 13"

    def test_cont_call_cc_abort(self) -> None:
        f: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x * 3)
        g: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x - 2)
        h = lambda x, abort: f(x) if x == 5 else abort(-1)

        do_c = lambda n: Cont.unit(n) | (lambda x: Cont.call_cc(lambda abort: h(x, abort))) | (lambda y: g(y))
        final_c: Callable[[int], str] = lambda x: f"Done: {x}"

        assert do_c(4).run(final_c) == "Done: -3"

    def test_cont_call_cc_abort_2(self) -> None:
        f: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x * 3)
        g: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x - 2)
        h = lambda x, abort: f(x) if x == 5 else abort(-1)

        do_c = lambda n: Cont.unit(n) | (lambda x: Cont.call_cc(lambda abort: h(x, abort) | (lambda y: g(y))))

        final_c: Callable[[int], str] = lambda x: f"Done: {x}"

        assert do_c(4).run(final_c) == "Done: -1"


class TestContFunctor(unittest.TestCase):
    def test_cont_functor_map(self) -> None:
        x: Cont[int, int] = Cont.unit(42)
        f: Callable[[int], int] = lambda x: x * 10

        assert x.map(f) == Cont.unit(420)

    def test_cont_functor_law_1(self) -> None:
        # fmap id = id
        x: Cont[int, int] = Cont.unit(42)

        assert x.map(identity) == x

    def test_cont_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        f: Callable[[int], int] = lambda x: x + 10
        g: Callable[[int], int] = lambda x: x * 10

        x: Cont[int, int] = Cont.unit(42)

        assert x.map(compose(f, g)) == x.map(g).map(f)


class TestContMonad(unittest.TestCase):
    def test_cont_monad_bind(self) -> None:
        m: Cont[int, int] = Cont.unit(42)
        f: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x * 10)

        assert m.bind(f) == Cont.unit(420)

    def test_cont_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x + 100000)
        x: int = 3

        assert Cont.unit(x).bind(f) == f(x)

    def test_cont_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m: Cont[str, str] = Cont.unit("move on up")

        assert m.bind(Cont.unit) == m

    def test_cont_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m: Cont[int, int] = Cont.unit(42)
        f: Callable[[int], Cont[int, int]] = lambda x: Cont.unit(x + 1000)
        g: Callable[[int], Cont[int, int]] = lambda y: Cont.unit(y * 42)

        assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))
