import unittest
from collections.abc import Callable

from oslash import List, StringWriter, Writer


class TestWriterMonad(unittest.TestCase):
    def test_writer_return(self) -> None:
        w = StringWriter.unit(42)
        assert w.run() == (42, "")

    def test_writer_unitint_log(self) -> None:
        IntWriter = Writer.create("IntWriter", int)
        w = IntWriter.unit(42)
        assert w.run() == (42, 0)

    def test_generic_writer_unit_uses_explicit_empty_log(self) -> None:
        assert Writer[int, list[str]].unit(42, empty_log=[]).run() == (42, [])
        assert Writer[int, None].unit(42, empty_log=None).run() == (42, None)

    def test_writer_map_preserves_log(self) -> None:
        writer = Writer(42, ["before"])
        assert writer.map(str).run() == ("42", ["before"])
        assert writer.map_with_log(lambda pair: (str(pair[0]), [*pair[1], "after"])).run() == (
            "42",
            ["before", "after"],
        )

    def test_writer_monad_bind(self) -> None:
        entry: str = "Multiplied by 10"
        f: Callable[[int], Writer[int, str]] = lambda x: StringWriter(x * 10, entry)
        m = StringWriter.unit(42).bind(f)
        assert m == StringWriter(420, entry)

    def test_writer_monad_law_left_identity(self) -> None:
        # return x >>= f == f x
        entry: str = "Added 100000 to %s"
        f: Callable[[int], Writer[int, str]] = lambda x: StringWriter(x + 100000, entry % x)
        a = StringWriter.unit(42).bind(f)
        b = f(42)
        assert a == b

    def test_writer_monad_law_right_identity(self) -> None:
        # m >>= return is no different than just m.
        a = StringWriter.unit(42).bind(StringWriter.unit)
        assert a == StringWriter.unit(42)

    def test_writer_monad_law_associativity(self) -> None:
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        add1000: str = "Added 1000 to %s"
        mul100: str = "Multiplied %s by 100"
        f: Callable[[int], Writer[int, str]] = lambda x: StringWriter(x + 1000, add1000 % x)
        g: Callable[[int], Writer[int, str]] = lambda y: StringWriter(y * 100, mul100 % y)
        a = StringWriter.unit(42).bind(f).bind(g)
        b = StringWriter.unit(42).bind(lambda x: f(x).bind(g))
        assert a == b

    def test_factory_list_logs_preserve_type_and_have_fresh_identities(self) -> None:
        list_writer = Writer.create("ListWriter", list[str])
        first = list_writer.unit(1)
        second = list_writer.unit(2)
        assert first.run() == (1, [])
        assert first.run()[1] is not second.run()[1]
        assert first.map(str).run() == ("1", [])
        assert first.bind(lambda value: list_writer(value + 1, ["entry"])).run() == (2, ["entry"])

    def test_factory_uses_monoid_empty(self) -> None:
        list_writer = Writer.create("MonoidWriter", List[str])
        assert list_writer.unit(1).run() == (1, List[str].empty())

    def test_default_factory_and_direct_construction(self) -> None:
        default_writer = Writer.create("DefaultWriter")
        assert default_writer.unit(1).run() == (1, "")
        assert StringWriter(1, "entry").run() == (1, "entry")
