import unittest
from collections.abc import Callable

from oslash.observable import Observable
from oslash.util import compose, identity


class TestObservable(unittest.TestCase):
    def test_observable_just(self) -> None:
        stream = Observable.just(42)

        result: list[str] = []

        def on_next(x: int) -> None:
            result.append(f"OnNext({x})")

        stream.subscribe(on_next)
        assert result == ["OnNext(42)"]

    def test_observable_just_map(self) -> None:
        mapper: Callable[[int], int] = lambda x: x * 10
        stream = Observable.just(42).map(mapper)

        result: list[str] = []

        def on_next(x: int) -> None:
            result.append(f"OnNext({x})")

        stream.subscribe(on_next)
        assert result == ["OnNext(420)"]

    def test_observable_just_flatmap(self) -> None:
        flat_mapper: Callable[[int], Observable[int]] = lambda x: Observable.just(x * 10)
        stream = Observable.just(42).flat_map(flat_mapper)

        result: list[str] = []

        def on_next(x: int) -> None:
            result.append(f"OnNext({x})")

        stream.subscribe(on_next)
        assert result == ["OnNext(420)"]

    def test_observable_filter(self) -> None:
        predicate: Callable[[int], bool] = lambda x: x < 100
        stream = Observable.just(42).filter(predicate)
        xs: list[str] = []

        def on_next(x: int) -> None:
            xs.append(f"OnNext({x})")

        stream.subscribe(on_next)
        assert xs == ["OnNext(42)"]

    def test_cont_call_cc(self) -> None:
        f: Callable[[int], Observable[int]] = lambda x: Observable.just(x * 3)
        g: Callable[[int], Observable[int]] = lambda x: Observable.just(x - 2)

        def h(x: int, on_next: Callable[[int], Observable[int]]) -> Observable[int]:
            return f(x) if x == 5 else on_next(-1)

        stream = Observable.just(5) | (lambda x: Observable.call_cc(lambda on_next: h(x, on_next))) | (lambda y: g(y))

        result: list[str] = []

        def on_result(x: int) -> None:
            result.append(f"Done: {x}")

        stream.subscribe(on_result)
        assert result == ["Done: 13"]


class TestObservableFunctor(unittest.TestCase):
    def test_cont_functor_map(self) -> None:
        x = Observable.unit(42)
        f: Callable[[int], int] = lambda x: x * 10

        assert x.map(f) == Observable.unit(420)

    def test_cont_functor_law_1(self) -> None:
        # fmap id = id
        x = Observable.unit(42)

        assert x.map(identity) == x

    def test_cont_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x: int) -> int:
            return x + 10

        def g(x: int) -> int:
            return x * 10

        x = Observable.unit(42)

        assert x.map(compose(f, g)) == x.map(g).map(f)


class TestObservableMonad(unittest.TestCase):
    def test_cont_monad_bind(self) -> None:
        m = Observable.unit(42)
        f: Callable[[int], Observable[int]] = lambda x: Observable.unit(x * 10)

        assert m.bind(f) == Observable.unit(420)

    def test_cont_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f: Callable[[int], Observable[int]] = lambda x: Observable.unit(x + 100000)
        x: int = 3

        assert Observable.unit(x).bind(f) == f(x)

    def test_cont_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m = Observable.unit("move on up")

        assert m.bind(Observable.unit) == m

    def test_cont_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = Observable.unit(42)
        f: Callable[[int], Observable[int]] = lambda x: Observable.unit(x + 1000)
        g: Callable[[int], Observable[int]] = lambda y: Observable.unit(y * 42)

        assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))
