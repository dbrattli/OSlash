import unittest
from typing import Tuple

import oslash.ioaction
from oslash import Put, Return, put_line, get_line
from oslash.util import Unit


class MyMock:
    """Mock for testing side effects"""

    def __init__(self) -> None:
        self.value = None  # type: str
        oslash.ioaction.pure_input = self.pure_input
        oslash.ioaction.pure_print = self.pure_print

    def pure_print(self, world: int, text: str) -> int:
        self.value = text
        return world + 1

    def pure_input(self, world: int) -> Tuple[int, str]:
        text = self.value
        new_world = world + 1
        return new_world, text


class TestPut(unittest.TestCase):

    def test_put_line(self) -> None:
        pm = MyMock()
        action = put_line("hello, world!")
        action()
        self.assertEqual(pm.value, "hello, world!")

    def test_put_return(self) -> None:
        pm = MyMock()
        action = Put("hello, world!", Return(Unit))
        action()
        self.assertEqual(pm.value, "hello, world!")
