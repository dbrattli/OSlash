# coding=utf-8
import unittest

from oslash.cont import Cont
from oslash.util import identity, compose, compose2, Unit

#pure = Cont.pure
unit = Cont.unit


class TestCont(unittest.TestCase):
    def test_cont_basic(self):
        add = lambda x, y: x+y
        add_cont = unit(add)

        self.assertEqual(
            42,
            add_cont.run(identity)(40, 2)
        )

    def test_cont_simple(self):
        f = lambda x: Cont(lambda c: c(x*3))
        g = lambda x: Cont(lambda c: c(x-2))

        h = lambda x: f(x) if x == 5 else g(x)

        do_c = unit(5) | h
        final_c = lambda x: "Done: %s" % x

        self.assertEqual(
            "Done: 15",
            do_c.run(final_c)
        )

    def test_cont_simpler(self):
        f = lambda x: unit(x*3)
        g = lambda x: unit(x-2)

        h = lambda x: f(x) if x == 5 else g(x)

        do_c = unit(4) | h
        final_c = lambda x: "Done: %s" % x

        self.assertEqual(
            "Done: 2",
            do_c.run(final_c)
        )


class TestReaderMonad(unittest.TestCase):

    def test_reader_monad_bind(self):
        m = unit(42)
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            unit(420)
        )
