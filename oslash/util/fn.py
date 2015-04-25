from functools import reduce

from typing import Tuple, Callable  # noqa


def compose(*funcs: "Tuple[Callable, ...]") -> Callable:
    """Compose multiple functions right to left.

    Composes zero or more functions into a functional composition. The
    functions are composed right to left. A composition of zero
    functions gives back the identity function.

    compose()(x) == x
    compose(f)(x) == f(x)
    compose(g, f)(x) == g(f(x))
    compose(h, g, f)(x) == h(g(f(x)))
    ...

    Returns the composed function.
    """
    def _compose(*args, **kw):
        """Reduce functions to a single function."""
        ret = reduce(lambda acc, x: lambda f: f(acc(x)),
                     funcs[::-1],
                     lambda f: f(*args, **kw))
        return ret(lambda x: x)
    return _compose

fmap = lambda f, g: compose(f, g)  # To force partial application

identity = compose()  # type: Callable
