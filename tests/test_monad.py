import unittest

from oslash import MonadWriter, StringWriter
from oslash.monadic import compose


class TestMonadMonadic(unittest.TestCase):
    def test_monad_monadic_compose(self) -> None:
        def half(x: int) -> StringWriter:
            return MonadWriter.tell(f"I just halved {x}!").bind(lambda _: StringWriter.unit(x // 2))

        quarter = compose(half, half)
        value, log = quarter(8).run()

        assert value == 2
        assert log == "I just halved 8!I just halved 4!"
