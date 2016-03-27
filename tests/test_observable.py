import unittest

from oslash.observable import Observable
from oslash.util import identity, compose

# pure = Cont.pure
just = Observable.just
call_cc = Observable.call_cc


class TestObservable(unittest.TestCase):
    def test_observable_just(self):
        stream = Observable.just(42)

        def on_next(x):
            return "OnNext(%s)" % x

        self.assertEqual("OnNext(42)", stream.subscribe(on_next))

    def test_observable_just_map(self):
        stream = Observable.just(42).map(lambda x: x*10)

        def on_next(x):
            return "OnNext(%s)" % x

        self.assertEqual("OnNext(420)", stream.subscribe(on_next))

    def test_observable_just_flatmap(self):
        stream = Observable.just(42).flat_map(lambda x: just(x*10))

        def on_next(x):
            return "OnNext(%s)" % x

        self.assertEqual("OnNext(420)", stream.subscribe(on_next))

    def test_observable_filter(self):
        stream = Observable.just(42).filter(lambda x: x < 100)
        xs = []

        def on_next(x):
            xs.append("OnNext(%s)" % x)
        stream.subscribe(on_next)
        self.assertEqual(["OnNext(42)"], xs)
