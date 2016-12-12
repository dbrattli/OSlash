import unittest

from oslash.cont import Cont
from oslash.util import identity, compose

# pure = Cont.pure
unit = Cont.unit
call_cc = Cont.call_cc


class TestCont(unittest.TestCase):
    def test_cont_pythagoras(self):
        add = lambda x, y: unit(x + y)
        square = lambda x: unit(x * x)

        pythagoras = lambda x, y: square(x) | (
            lambda xx: (square(y) | (
                lambda yy: add(xx, yy))))

        self.assertEqual(32, pythagoras(4, 4)(identity))

    def test_cont_basic(self):
        add = lambda x, y: x+y
        add_cont = unit(add)

        self.assertEqual(
            42,
            add_cont(identity)(40, 2)
        )

    def test_cont_simple(self):
        f = lambda x: unit(x*3)
        g = lambda x: unit(x-2)

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

    def test_cont_call_cc(self):
        f = lambda x: unit(x*3)
        g = lambda x: unit(x-2)

        h = lambda x, abort: f(x) if x == 5 else abort(-1)

        do_c = lambda n: unit(n) | (
            lambda x: call_cc(lambda abort: h(x, abort))) | (
                lambda y: g(y))
        final_c = lambda x: "Done: %s" % x

        self.assertEqual(
            "Done: 13",
            do_c(5).run(final_c)
        )

    def test_cont_call_cc_abort(self):
        f = lambda x: unit(x*3)
        g = lambda x: unit(x-2)

        h = lambda x, abort: f(x) if x == 5 else abort(-1)

        do_c = lambda n: unit(n) | (
            lambda x: call_cc(lambda abort: h(x, abort))) | (
                lambda y: g(y))
        final_c = lambda x: "Done: %s" % x

        self.assertEqual(
            "Done: -3",
            do_c(4).run(final_c)
        )

    def test_cont_call_cc_abort_2(self):
        f = lambda x: unit(x*3)
        g = lambda x: unit(x-2)
        h = lambda x, abort: f(x) if x == 5 else abort(-1)

        do_c = lambda n: unit(n) | (
            lambda x: call_cc(lambda abort: h(x, abort) | (
                lambda y: g(y))))

        final_c = lambda x: "Done: %s" % x

        self.assertEqual(
            "Done: -1",
            do_c(4).run(final_c)
        )


class TestContFunctor(unittest.TestCase):

    def test_cont_functor_map(self):
        x = unit(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.map(f),
            unit(420)
        )

    def test_cont_functor_law_1(self):
        # fmap id = id
        x = unit(42)

        self.assertEqual(
            x.map(identity),
            x
        )

    def test_cont_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = unit(42)

        self.assertEquals(
            x.map(compose(f, g)),
            x.map(g).map(f)
        )


class TestContMonad(unittest.TestCase):

    def test_cont_monad_bind(self):
        m = unit(42)
        f = lambda x: unit(x*10)

        self.assertEqual(
            m.bind(f),
            unit(420)
        )

    def test_cont_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: unit(x+100000)
        x = 3

        self.assertEqual(
            unit(x).bind(f),
            f(x)
        )

    def test_cont_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = unit("move on up")

        self.assertEqual(
            m.bind(unit),
            m
        )

    def test_cont_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = unit(42)
        f = lambda x: unit(x+1000)
        g = lambda y: unit(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )
