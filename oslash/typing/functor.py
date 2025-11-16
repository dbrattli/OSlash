"""Functor Protocol.

We use Protocol instead of ABC because:
1. Structural subtyping: Any class implementing these methods
   is automatically a Functor, no inheritance required
2. Better type checker support: Protocols work better with pyright
3. More Pythonic: Duck typing with static type safety
4. Runtime checking: @runtime_checkable allows isinstance checks
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from typing import Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class Functor[T](Protocol):
    """The Functor class is used for types that can be mapped over.

    Instances of Functor should satisfy the following laws:

    Haskell:
    fmap id  ==  id
    fmap (f . g)  ==  fmap f . fmap g

    Python:
    x.map(id) == id(x)
    x.map(compose(f, g)) == x.map(g).map(f)

    The instances of Functor for lists, Maybe and IO satisfy these laws.
    """

    @abstractmethod
    def map[U](self, fn: Callable[[T], U]) -> Functor[U]:
        """Map a function over wrapped values.

        Map knows how to apply functions to values that are wrapped in
        a context.
        """
        ...
