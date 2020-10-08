#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from oslash.list import List
from oslash.do import do, let, guard


class TestDo(unittest.TestCase):
    def test_do_list_basic(self):
        l = lambda *items: List.from_iterable(items)
        out1 = do(let(a=l(3, 10, 6)),
                  let(b=l(100, 200)),
                  lambda e: List.unit(e.a + e.b))
        out2 = l(3, 10, 6) | (lambda a:
               l(100, 200) | (lambda b:
               List.unit(a + b)))
        self.assertEqual(out1, out2)

    def test_do_list_pythag(self):
        r = lambda low, high: List.from_iterable(range(low, high))
        out1 = do(let(z=r(1, 21)),
                  let(x=lambda e: r(1, e.z+1)),
                  let(y=lambda e: r(e.x, e.z+1)),
                  lambda e: guard(List, e.x*e.x + e.y*e.y == e.z*e.z),
                  lambda e: List.unit((e.x, e.y, e.z)))
        out2 = r(1, 21)  | (lambda z:
               r(1, z+1) | (lambda x:
               r(x, z+1) | (lambda y:
               guard(List, x*x + y*y == z*z) >>
               List.unit((x,y,z)))))
        self.assertEqual(out1, out2)

    # TODO: add more tests


class TestDoErrors(unittest.TestCase):
    def test_do_invalid_input(self):
        try:
            do("some invalid input")
        except TypeError:
            pass
        else:
            assert False

    def test_do_scoping_correct(self):
        try:
            l = lambda *items: List.from_iterable(items)
            do(let(a=l(1, 2, 3)),
               let(b=lambda e: List.unit(e.a)),
               lambda e: List.unit(e.a * e.b))
        except AttributeError:
            assert False

    def test_do_scoping_invalid(self):
        try:
            l = lambda *items: List.from_iterable(items)
            do(let(a=lambda e: List.unit(e.b)),
               let(b=l(1, 2, 3)),
               lambda e: List.unit(e.a * e.b))
        except AttributeError as err:
            pass
        else:
            assert False
