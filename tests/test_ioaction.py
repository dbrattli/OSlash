import unittest

import oslash.ioaction
from oslash import Put, Return, put_line
from oslash.util import Unit


class MyMock:
    """Mock for testing side effects"""

    def __init__(self) -> None:
        self.value: str | None = None
        oslash.ioaction.pure_input = self.pure_input
        oslash.ioaction.pure_print = self.pure_print

    def pure_print(self, world: int, text: str) -> int:
        self.value = text
        return world + 1

    def pure_input(self, world: int) -> tuple[int, str]:
        text: str = self.value or ""  # Provide default for None case
        new_world: int = world + 1
        return new_world, text


class TestPut(unittest.TestCase):
    def test_put_line(self) -> None:
        pm: MyMock = MyMock()
        action = put_line("hello, world!")
        action()
        assert pm.value == "hello, world!"

    def test_put_return(self) -> None:
        pm: MyMock = MyMock()
        action: Put[tuple[()]] = Put("hello, world!", Return(Unit))
        action()
        assert pm.value == "hello, world!"
