import unittest
from typing import Any

from oslash.list import List
from oslash.util import compose, fmap, identity

pure: Any = List.pure
unit: Any = List.unit  # type: ignore[assignment]
empty: Any = List.empty  # type: ignore[assignment]


class TestList(unittest.TestCase):
    def test_list_null(self) -> None:
        xs: List[Any] = empty()
        assert xs.null()

    def test_list_not_null_after_cons_and_tail(self) -> None:
        xs: List[Any] = empty().cons(1).tail()
        assert xs.null()

    def test_list_not_null_after_cons(self) -> None:
        xs: List[Any] = empty().cons(1)
        assert not xs.null()

    def test_list_head(self) -> None:
        x: Any = empty().cons(42).head()
        assert x == 42

    def test_list_tail_head(self) -> None:
        xs: List[Any] = empty().cons("b").cons("a")
        assert xs.head() == "a"

    def test_list_tail_tail_null(self) -> None:
        xs: List[Any] = empty().cons("b").cons("a")
        assert xs.tail().tail().null()

    def test_list_list(self) -> None:
        xs: List[Any] = empty().cons(empty().cons(42))
        assert xs.head() == empty().cons(42)

    def test_list_length_empty(self) -> None:
        xs: List[Any] = empty()
        assert len(xs) == 0

    def test_list_length_non_empty(self) -> None:
        xs: List[Any] = List.unit(42)  # type: ignore[var-annotated]
        assert len(xs) == 1

    def test_list_length_multiple(self) -> None:
        xs: List[Any] = List.from_iterable(range(42))  # type: ignore[var-annotated]
        assert len(xs) == 42

    def test_list_append_empty(self) -> None:
        xs: List[Any] = empty()
        ys: List[Any] = List.unit(42)  # type: ignore[var-annotated]
        zs: List[Any] = xs.append(ys)
        assert ys == zs

    def test_list_append_empty_other(self) -> None:
        xs: List[Any] = List.unit(42)  # type: ignore[var-annotated]
        ys: List[Any] = empty()
        zs: List[Any] = xs.append(ys)
        assert xs == zs

    def test_list_append_non_empty(self) -> None:
        xs: List[Any] = List.from_iterable(range(5))  # type: ignore[var-annotated]
        ys: List[Any] = List.from_iterable(range(5, 10))  # type: ignore[var-annotated]
        zs: List[Any] = xs.append(ys)
        assert List.from_iterable(range(10)) == zs  # type: ignore[arg-type]


class TestListFunctor(unittest.TestCase):
    def test_list_functor_map(self) -> None:
        # fmap f (return v) = return (f v)
        x: List[Any] = unit(42)
        f = lambda x: x * 10  # type: ignore[misc]

        assert x.map(f) == unit(420)  # type: ignore[arg-type]

        y: List[Any] = List.from_iterable([1, 2, 3, 4])  # type: ignore[var-annotated]
        g = lambda x: x * 10  # type: ignore[misc]

        assert y.map(g) == List.from_iterable([10, 20, 30, 40])  # type: ignore[arg-type]

    def test_list_functor_law_1(self) -> None:
        # fmap id = id

        # Singleton list using return
        x: List[Any] = unit(42)
        assert x.map(identity) == x

        # Empty list
        y: List[Any] = empty()
        assert y.map(identity) == y

        # Long list
        z: List[Any] = List.from_iterable(range(42))  # type: ignore[var-annotated]
        assert z.map(identity) == z

    def test_list_functor_law2(self) -> None:
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x: int) -> int:
            return x + 10

        def g(x: int) -> int:
            return x * 10

        # Singleton list
        x: List[Any] = unit(42)
        assert x.map(compose(f, g)) == x.map(g).map(f)

        # Empty list
        y: List[Any] = List.empty()  # type: ignore[var-annotated]
        assert y.map(compose(f, g)) == y.map(g).map(f)

        # Long list
        z: List[Any] = List.from_iterable(range(42))  # type: ignore[var-annotated]
        assert z.map(compose(f, g)) == z.map(g).map(f)


class TestListApplicative(unittest.TestCase):
    def test_list_applicative_law_functor(self) -> None:
        # pure f <*> x = fmap f x
        f = lambda x: x * 42  # type: ignore[misc]

        x: List[Any] = unit(42)
        assert pure(f).apply(x) == x.map(f)  # type: ignore[arg-type]

        # Empty list
        z: List[Any] = empty()
        assert pure(f).apply(z) == z.map(f)  # type: ignore[arg-type]

        # Long list
        z = List.from_iterable(range(42))  # type: ignore[assignment]
        assert pure(f).apply(z) == z.map(f)  # type: ignore[arg-type]

    def test_list_applicative_law_identity(self) -> None:
        # pure id <*> v = v

        # Singleton list
        x: List[Any] = unit(42)
        assert pure(identity).apply(x) == x

        # Empty list
        y: List[Any] = List.empty()  # type: ignore[var-annotated]
        assert pure(identity).apply(y) == y

        # Log list
        y = List.from_iterable(range(42))  # type: ignore[assignment]
        assert pure(identity).apply(y) == y

    def test_identity_applicative_law_composition(self) -> None:
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u: List[Any] = pure(lambda x: x * 42)  # type: ignore[misc,var-annotated]
        v: List[Any] = pure(lambda x: x + 42)  # type: ignore[misc,var-annotated]

        # Singleton list
        w: List[Any] = unit(42)
        assert pure(fmap).apply(u).apply(v).apply(w) == u.apply(v.apply(w))

    def test_identity_applicative_law_composition_empty(self) -> None:
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u: List[Any] = pure(lambda x: x * 42)  # type: ignore[misc,var-annotated]
        v: List[Any] = pure(lambda x: x + 42)  # type: ignore[misc,var-annotated]

        # Empty list
        w: List[Any] = empty()
        assert pure(fmap).apply(u).apply(v).apply(w) == u.apply(v.apply(w))

    def test_identity_applicative_law_composition_range(self) -> None:
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        u: List[Any] = pure(lambda x: x * 42)  # type: ignore[misc,var-annotated]
        v: List[Any] = pure(lambda x: x + 42)  # type: ignore[misc,var-annotated]

        # Long list
        w: List[Any] = List.from_iterable(range(42))  # type: ignore[var-annotated]
        assert pure(fmap).apply(u).apply(v).apply(w) == u.apply(v.apply(w))

    def test_list_applicative_binary_func_singleton(self) -> None:
        f = lambda x, y: x + y  # type: ignore[misc]
        v: List[Any] = unit(2)
        w: List[Any] = unit(40)

        assert pure(f).apply(v).apply(w) == unit(42)

    def test_list_applicative_unary_func(self) -> None:
        f = lambda x: x * 2  # type: ignore[misc]
        v: List[Any] = unit(21)

        assert pure(f).apply(v) == unit(42)

    def test_list_applicative_binary_func(self) -> None:
        f = lambda x, y: x + y  # type: ignore[misc]
        v: List[Any] = List.from_iterable([1, 2])  # type: ignore[var-annotated]
        w: List[Any] = List.from_iterable([4, 8])  # type: ignore[var-annotated]

        assert pure(f).apply(v).apply(w) == List.from_iterable([5, 9, 6, 10])  # type: ignore[arg-type]

    def test_list_applicative_empty_func(self) -> None:
        v: List[Any] = unit(42)
        w: List[Any] = List.from_iterable([1, 2, 3])  # type: ignore[var-annotated]

        assert empty().apply(v).apply(w) == empty()

    def test_list_applicative_binary_func_empty_arg_1(self) -> None:
        f = lambda x, y: x + y  # type: ignore[misc]
        v: List[Any] = unit(42)
        e: List[Any] = empty()

        assert pure(f).apply(e).apply(v) == empty()

    def test_list_applicative_binary_func_empty_arg_2(self) -> None:
        f = lambda x, y: x + y  # type: ignore[misc]
        v: List[Any] = unit(42)
        e: List[Any] = empty()

        assert pure(f).apply(v).apply(e) == empty()


class TestListMonad(unittest.TestCase):
    def test_list_monad_bind(self) -> None:
        m: List[Any] = unit(42)
        f = lambda x: unit(x * 10)  # type: ignore[misc]

        assert m.bind(f) == unit(420)  # type: ignore[arg-type]

    def test_list_monad_empty_bind(self) -> None:
        m: List[Any] = empty()
        f = lambda x: unit(x * 10)  # type: ignore[misc]

        assert m.bind(f) == empty()  # type: ignore[arg-type]

    def test_list_monad_law_left_identity(self) -> None:
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x + 100000)  # type: ignore[misc]
        v: int = 42

        assert unit(v).bind(f) == f(v)

    def test_list_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.

        m: List[Any] = unit("move on up")

        assert m.bind(unit) == m

    def test_list_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        f = lambda x: unit(x + 1000)  # type: ignore[misc]
        g = lambda y: unit(y * 42)  # type: ignore[misc]

        m: List[Any] = unit(42)
        assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))  # type: ignore[misc]

    def test_list_monad_law_associativity_empty(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        f = lambda x: unit(x + 1000)  # type: ignore[misc]
        g = lambda y: unit(y * 42)  # type: ignore[misc]

        # Empty list
        m: List[Any] = empty()
        assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))  # type: ignore[misc]

    def test_list_monad_law_associativity_range(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        f = lambda x: unit(x + 1000)  # type: ignore[misc]
        g = lambda y: unit(y * 42)  # type: ignore[misc]

        # Long list
        m: List[Any] = List.from_iterable(range(42))  # type: ignore[var-annotated]
        assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))  # type: ignore[misc]


class TestListConstruction(unittest.TestCase):
    """Tests for direct List construction (issue #34)."""

    def test_list_direct_construction_with_list(self) -> None:
        # Test direct construction with Python list
        lst: List[int] = List([1, 2, 3])
        assert len(lst) == 3
        assert lst.head() == 1
        assert lst == List.from_iterable([1, 2, 3])

    def test_list_direct_construction_with_tuple(self) -> None:
        # Test direct construction with tuple
        lst: List[int] = List((4, 5, 6))
        assert len(lst) == 3
        assert lst.head() == 4
        assert lst == List.from_iterable([4, 5, 6])

    def test_list_direct_construction_with_range(self) -> None:
        # Test direct construction with range
        lst: List[int] = List(range(5))
        assert len(lst) == 5
        assert lst.head() == 0
        assert lst == List.from_iterable(range(5))

    def test_list_direct_construction_with_generator(self) -> None:
        # Test direct construction with generator
        lst: List[int] = List(x * 2 for x in range(3))
        assert len(lst) == 3
        assert lst == List.from_iterable([0, 2, 4])

    def test_list_direct_construction_empty(self) -> None:
        # Test direct construction with no arguments
        lst: List[Any] = List()
        assert lst.null()
        assert len(lst) == 0
        assert lst == List.empty()

    def test_list_direct_construction_empty_list(self) -> None:
        # Test direct construction with empty list
        lst: List[Any] = List([])
        assert lst.null()
        assert len(lst) == 0
        assert lst == List.empty()

    def test_list_direct_construction_single_element(self) -> None:
        # Test direct construction with single element
        lst: List[int] = List([42])
        assert not lst.null()
        assert len(lst) == 1
        assert lst.head() == 42
        assert lst == List.unit(42)

    def test_list_construction_equivalence(self) -> None:
        # Test that both construction methods are equivalent
        data = [1, 2, 3, 4, 5]
        direct: List[int] = List(data)
        from_iterable: List[int] = List.from_iterable(data)
        assert direct == from_iterable


class TestListOperators(unittest.TestCase):
    """Tests for List operator overloading (issue #34)."""

    def test_list_rmod_operator_basic(self) -> None:
        # Test % operator with simple function
        lst: List[int] = List([1, 2, 3])
        result = (lambda x: x + 1) % lst
        assert result == List([2, 3, 4])

    def test_list_rmod_operator_multiply(self) -> None:
        # Test % operator with multiplication
        lst: List[int] = List([1, 2, 3])
        result = (lambda x: x * 2) % lst
        assert result == List([2, 4, 6])

    def test_list_rmod_operator_empty(self) -> None:
        # Test % operator with empty list
        lst: List[int] = List()
        result = (lambda x: x + 1) % lst
        assert result == List()
        assert result.null()

    def test_list_rmod_operator_single_element(self) -> None:
        # Test % operator with single element
        lst: List[int] = List([42])
        result = (lambda x: x * 10) % lst
        assert result == List([420])

    def test_list_rmod_operator_string(self) -> None:
        # Test % operator with string transformation
        lst: List[str] = List(["a", "b", "c"])
        result = (lambda s: s.upper()) % lst
        assert result == List(["A", "B", "C"])

    def test_list_rmod_operator_type_change(self) -> None:
        # Test % operator changing type
        lst: List[int] = List([1, 2, 3])
        result = (lambda x: str(x)) % lst
        assert result == List(["1", "2", "3"])

    def test_list_rmod_operator_equivalence_to_map(self) -> None:
        # Test that % is equivalent to map
        lst: List[int] = List([1, 2, 3, 4, 5])
        f = lambda x: x**2  # type: ignore[misc]
        rmod_result = f % lst
        map_result = lst.map(f)
        assert rmod_result == map_result

    def test_list_rmod_operator_composition(self) -> None:
        # Test % operator with composed functions
        lst: List[int] = List([1, 2, 3])
        result = (lambda x: x + 1) % ((lambda x: x * 2) % lst)
        assert result == List([3, 5, 7])

    def test_list_rmod_operator_long_list(self) -> None:
        # Test % operator with longer list
        lst: List[int] = List(range(10))
        result = (lambda x: x * 2) % lst
        expected = List(range(0, 20, 2))
        assert result == expected
