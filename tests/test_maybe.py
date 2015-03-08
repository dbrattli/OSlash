import unittest

from ø.maybe import Maybe, Just, Nothing


class TestMaybe(unittest.TestCase):
    def test_just_fmap(self):
        b = Just(21).fmap(lambda x: x*2)
        self.assertEquals(b, Just(42))

    def test_just_functor_law1(self):
        """fmap id = id"""
        _id = lambda x: x
        self.assertEquals(Just(3).fmap(_id), Just(3))

    def test_just_functor_law2(self):
        """fmap (f . g) x = fmap f (fmap g x)"""
        def f(x):
            return x+10

        def g(x):
            return x*10

        self.assertEquals(
            Just(42).fmap(f).fmap(g),
            Just(42).fmap(lambda x: g(f(x)))
        )

    def test_just_applicative_1(self):
        a = Just(lambda x, y: x+y).apply(Just(2)).apply(Just(40))
        self.assertNotEquals(a, Nothing())
        self.assertEquals(a, Just(42))

    def test_just_applicative_2(self):
        a = Just(lambda x, y: x+y).apply(Nothing()).apply(Just(42))
        self.assertEquals(a, Nothing())

    def test_just_applicative_3(self):
        a = Just(lambda x, y: x+y).apply(Just(42)).apply(Nothing())
        self.assertEquals(a, Nothing())

    def test_maybe_monoid_nothing_mappend_just(self):
        a = Nothing().mappend(Just("Python"))
        self.assertEquals(a, Just("Python"))

    def test_maybe_monoid_just_mappend_nothing(self):
        a = Just("Python").mappend(Nothing())
        self.assertEquals(a, Just("Python"))

    def test_maybe_monoid_just_mappend_just(self):
        a = Just("Python").mappend(Just(" rocks!"))
        self.assertEquals(a, Just("Python rocks!"))

    def test_maybe_monoid_mconcat(self):
        a = Maybe.mconcat([Just(2), Just(40)])
        self.assertEquals(a, Just(42))

    def test_nothing_fmap(self):
        a = Nothing().fmap(lambda x: x+2)
        self.assertEquals(a, Nothing())

    def test_nothing_functor_law1(self):
        """fmap id = id"""
        _id = lambda x: x
        self.assertEquals(Nothing().fmap(_id), Nothing())

    def test_nothing_functor_law2(self):
        """fmap (f . g) x = fmap f (fmap g x)"""
        def f(x):
            return x+10

        def g(x):
            return x*10

        self.assertEquals(
            Nothing().fmap(g).fmap(f),
            Nothing().fmap(lambda x: g(f(x)))
        )

