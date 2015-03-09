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
        a = Just.pure(lambda x, y: x+y).apply(Just(2)).apply(Just(40))
        self.assertNotEquals(a, Nothing())
        self.assertEquals(a, Just(42))

    def test_just_applicative_2(self):
        a = Just.pure(lambda x, y: x+y).apply(Nothing()).apply(Just(42))
        self.assertEquals(a, Nothing())

    def test_just_applicative_3(self):
        a = Just.pure(lambda x, y: x+y).apply(Just(42)).apply(Nothing())
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

    def test_maybe_monad_bind(self):
        m = Just(42).bind(lambda x: Just(x*10))
        self.assertEqual(m, Just(420))

    def test_maybe_monad_nothing_bind(self):
        """Nothing >>= \\x -> return (x*10)"""
        m = Nothing().bind(lambda x: Just(x*10))
        self.assertEqual(m, Nothing())

    def test_maybe_monad_law_left_identity(self):
        # return 3 >>= (\x -> Just (x+100000))
        a = Just(3).bind(lambda x: Just(x+100000))
        # (\x -> Just (x+100000)) 3
        b = (lambda x: Just(x+100000))(3)
        self.assertEqual(a, b)

    def test_maybe_monad_law_right_identity(self):
        # Just "move on up" >>= (\x -> return x)
        a = Just("move on up").bind(lambda x: Just(x))
        self.assertEqual(a, Just("move on up"))

    def test_maybe_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        a = Just(42).bind(lambda x: Just(x+1000)).bind(lambda y: Just(y*100))
        b = Just(42).bind(lambda x: Just(x+1000).bind(lambda y: Just(y*100)))
        self.assertEqual(a, b)
