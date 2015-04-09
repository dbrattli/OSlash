import unittest

from oslash import Put, IO, put_line, get_line


class MyMock:
    """Mock for testing side effects"""

    def __init__(self):
        self.value = None

    def print(self, string):
        self.value = string

    def input(self):
        return self.value


class TestPut(unittest.TestCase):

    def test_put_line(self):
        pm = MyMock()
        io = put_line("hello, world!")
        io(print=pm.print)
        self.assertEqual(pm.value, "hello, world!")

    def test_put_return(self):
        pm = MyMock()
        p = Put.unit("hello, world!", IO(()))
        p(print=pm.print)
        self.assertEqual(pm.value, "hello, world!")


