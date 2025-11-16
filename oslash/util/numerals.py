"""Lambda calculus and Church encoding.

* http://en.wikipedia.org/wiki/Church_encoding
* http://www.cs.bham.ac.uk/~axj/pub/papers/lambda-calculus.pdf
* http://vanderwijk.info/blog/pure-lambda-calculus-python/
* http://eflorenzano.com/blog/2008/11/20/lambda-calculus/

Just for the fun of it.
"""

from __future__ import annotations

from collections.abc import Callable

# Type aliases for Church encodings
type ChurchBoolean[T] = Callable[[T], Callable[[T], T]]
type ChurchNumeral[T] = Callable[[Callable[[T], T]], Callable[[T], T]]


# Basic combinators
def identity[T](x: T) -> T:
    """Identity combinator."""
    return x


def self_apply[T](s: Callable[[T], T]) -> T:
    """Self-application combinator."""
    return s(s)  # type: ignore[arg-type]


# Selectors
def select_first[T](first: T) -> Callable[[T], T]:
    """Select first element."""
    return lambda second: first


def select_second[T](first: T) -> Callable[[T], T]:
    """Select second element."""
    return lambda second: second


# Pair constructor
def make_pair[T](first: T) -> Callable[[T], Callable[[ChurchBoolean[T]], T]]:
    """Make a pair."""
    return lambda second: lambda func: func(first)(second)


# Application
def apply[T, U](func: Callable[[T], U]) -> Callable[[T], U]:
    """Apply a function to an argument."""
    return lambda arg: func(arg)


# Conditional
def cond[T](e1: T) -> Callable[[T], Callable[[ChurchBoolean[T]], T]]:
    """Conditional expression."""
    return lambda e2: lambda c: c(e1)(e2)


# Booleans
def true[T](first: T) -> Callable[[T], T]:
    """Church boolean true."""
    return select_first(first)


def false[T](first: T) -> Callable[[T], T]:
    """Church boolean false."""
    return select_second(first)


# If-then-else
def iff[T](c: ChurchBoolean[T], a: T, b: T) -> T:
    """If-then-else expression."""
    return c(a)(b)


# Boolean operations
def not_[T](x: ChurchBoolean[T]) -> ChurchBoolean[T]:
    """Logical NOT."""
    return cond(false)(true)(x)  # type: ignore[arg-type,return-value]


def and_[T](x: ChurchBoolean[T]) -> Callable[[ChurchBoolean[T]], ChurchBoolean[T]]:
    """Logical AND."""
    return lambda y: x(y)(false)  # type: ignore[arg-type,return-value]


def or_[T](x: ChurchBoolean[T]) -> Callable[[ChurchBoolean[T]], ChurchBoolean[T]]:
    """Logical OR."""
    return lambda y: x(true)(y)  # type: ignore[arg-type,return-value]


# Church numerals
# succ = λn.λf.λx.f (n f x)
def succ[T](n: ChurchNumeral[T]) -> ChurchNumeral[T]:
    """Successor function for Church numerals."""
    return lambda f: lambda x: f(n(f)(x))


def zero[T](f: Callable[[T], T]) -> Callable[[T], T]:
    """Church numeral zero."""
    return identity


def one[T](f: Callable[[T], T]) -> Callable[[T], T]:
    """Church numeral one."""
    return lambda x: f(x)


# Derived numerals
two: ChurchNumeral[int] = succ(one)
three: ChurchNumeral[int] = succ(two)


def is_zero[T](n: ChurchNumeral[T]) -> ChurchBoolean[T]:
    """Test if Church numeral is zero."""
    return n(select_first)  # type: ignore[arg-type,return-value]


# Convert Church numeral to Python int
def to_int(n: ChurchNumeral[int]) -> int:
    """Convert Church numeral to Python int."""
    return n(lambda x: x + 1)(0)


def printl(n: ChurchNumeral[int]) -> int:
    """Print Church numeral as Python int."""
    return n(lambda x: x + 1)(0)
