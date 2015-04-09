import unittest

from oslash import Monad, Writer, MonadWriter

compose = Monad.compose


class TestMonadMonadic(unittest.TestCase):

    def test_monad_monadic_compose(self):
        unit, tell = Writer.unit, MonadWriter.tell

        half = lambda x: tell("I just halved %s!" % x).bind(lambda _: unit(x//2))

        quarter = compose(half, half)
        value, log = quarter(8).run()

        self.assertEqual(2, value)
        self.assertEqual("I just halved 8!I just halved 4!", log)
