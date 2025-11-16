import unittest
from collections.abc import Callable
from typing import Any

from oslash import StringWriter, Writer


class TestWriterMonad(unittest.TestCase):
    def test_writer_return(self) -> None:
        w = StringWriter.unit(42)
        assert w.run() == (42, "")

    def test_writer_unitint_log(self) -> None:
        IntWriter: type[Any] = Writer.create("IntWriter", int)  # type: ignore[assignment]
        w: Any = IntWriter.unit(42)  # type: ignore[attr-defined]
        assert w.run() == (42, 0)

    def test_writer_monad_bind(self) -> None:
        entry: str = "Multiplied by 10"
        f: Callable[[int], StringWriter] = lambda x: StringWriter(x * 10, entry)
        m = StringWriter.unit(42).bind(f)
        assert m == StringWriter(420, entry)

    def test_writer_monad_law_left_identity(self) -> None:
        # return x >>= f == f x
        entry: str = "Added 100000 to %s"
        f: Callable[[int], StringWriter] = lambda x: StringWriter(x + 100000, entry % x)
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
        f: Callable[[int], StringWriter] = lambda x: StringWriter(x + 1000, add1000 % x)
        g: Callable[[int], StringWriter] = lambda y: StringWriter(y * 100, mul100 % y)
        a = StringWriter.unit(42).bind(f).bind(g)
        b = StringWriter.unit(42).bind(lambda x: f(x).bind(g))
        assert a == b
