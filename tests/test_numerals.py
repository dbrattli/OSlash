import unittest

from oslash.util.numerals import *  # noqa


class TestNumerals(unittest.TestCase):
    def test_iff_true(self):
        self.assertEqual(
            iff(true, 1, 2),
            1
        )

    def test_iff_false(self):
        self.assertEqual(
            iff(false, 1, 2),
            2
        )

    def test_printl_zero(self):
        self.assertEqual(
            printl(zero),
            0
        )

    def test_printl_one(self):
        self.assertEqual(
            printl(one),
            1
        )

    def test_succ_zero(self):
        self.assertEqual(
            printl(succ(zero)),
            1
        )
