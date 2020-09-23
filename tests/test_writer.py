import unittest

from oslash import Writer, StringWriter


class TestWriterMonad(unittest.TestCase):
    def test_writer_return(self):
        w = StringWriter.unit(42)
        self.assertEqual(w.run(), (42, ""))

    def test_writer_unitint_log(self):
        IntWriter = Writer.create("IntWriter", int)
        w = IntWriter.unit(42)
        self.assertEqual(w.run(), (42, 0))

    def test_writer_monad_bind(self):
        entry = "Multiplied by 10"
        m = StringWriter.unit(42).bind(lambda x: StringWriter(x*10, entry))
        self.assertEqual(m, StringWriter(420, entry))

    def test_writer_monad_law_left_identity(self):
        # return x >>= f == f x
        entry = "Added 100000 to %s"
        a = StringWriter.unit(42).bind(lambda x: StringWriter(x+100000, entry % x))
        b = (lambda x: StringWriter(x+100000, entry % x))(42)
        self.assertEqual(a, b)

    def test_writer_monad_law_right_identity(self):
        # m >>= return is no different than just m.
        a = StringWriter.unit(42).bind(StringWriter.unit)
        self.assertEqual(a, StringWriter.unit(42))

    def test_writer_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        add1000 = "Added 1000 to %s"
        mul100 = "Multiplied %s by 100"
        a = StringWriter.unit(42).bind(
            lambda x: StringWriter(x+1000, add1000 % x)).bind(
            lambda y: StringWriter(y*100, mul100 % y))
        b = StringWriter.unit(42).bind(
            lambda x: StringWriter(x+1000, add1000 % x).bind(
                lambda y: StringWriter(y*100, mul100 % y)
            ))
        self.assertEqual(a, b)
