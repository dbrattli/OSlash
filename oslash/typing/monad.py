r"""The Monad Protocol.

All instances of the Monad typeclass should obey the three monad laws:

    1) Left identity: return a >>= f = f a
    2) Right identity: m >>= return = m
    3) Associativity: (m >>= f) >>= g = m >>= (\x -> f x >>= g)

We use Protocol instead of ABC because:
1. Structural subtyping: Any class implementing these methods
   is automatically a Monad, no inheritance required
2. Better type checker support: Protocols work better with pyright
3. More Pythonic: Duck typing with static type safety
4. Runtime checking: @runtime_checkable allows isinstance checks
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol

from typing_extensions import runtime_checkable

if TYPE_CHECKING:
    from typing import Self


@runtime_checkable
class Monad[T](Protocol):
    """Monad protocol"""

    @abstractmethod
    def bind[U](self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        """Monad bind method.

        Python: bind(self: Monad[A], func: Callable[[A], Monad[B]]) -> Monad[B]
        Haskell: (>>=) :: m a -> (a -> m b) -> m b

        This is the mother of all methods. It's hard to describe what it
        does, because it can be used for pretty much anything:

        * Transformation, for projecting Monadic values and functions.
        * Composition, for composing monadic functions.
        * Chaining, for chaining of functions as a monadic value.
        * Combining, for combining monadic values.
        * Sequencing, of Monadic functions.
        * Flattening, of nested Monadic values.
        * Variable substitution, assign values to variables.

        The Monad doesn't specify what is happening, only that whatever
        is happening satisfies the laws of associativity and identity.

        Returns a new Monad.
        """
        ...

    @classmethod
    @abstractmethod
    def unit(cls, value: T) -> Self:
        """Wrap a value in a default context.

        Haskell: return :: a -> m a .

        Inject a value into the monadic type. Since return is a reserved
        word in Python, we align with Scala and use the name unit
        instead.
        """
        ...
