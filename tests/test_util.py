import unittest

from oslash.util import compose, identity


class TestCompose(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(42, identity(42))

    def test_compose_0(self):
        f_id = compose()
        self.assertEqual(42, f_id(42))

    def test_compose_1(self):
        f = lambda x: x*42
        g = compose(f)
        self.assertEqual(420, g(10))

    def test_compose_2(self):
        f = lambda x: x*42
        g = lambda y: y+10
        h = compose(g, f)
        self.assertEqual(430, h(10))

    def test_compose_3(self):
        f = lambda x: x*42
        g = lambda y: y+10
        h = lambda z: z/2
        i = compose(h, g, f)
        self.assertEqual(215, i(10))

