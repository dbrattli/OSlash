# Functors, Applicatives, And Monads in Python

[![CI](https://github.com/dbrattli/OSlash/workflows/CI/badge.svg)](https://github.com/dbrattli/OSlash/actions)
[![PyPI](https://img.shields.io/pypi/v/oslash.svg)](https://pypi.org/project/oslash/)
[![Python Version](https://img.shields.io/pypi/pyversions/oslash.svg)](https://pypi.org/project/oslash/)
[![License](https://img.shields.io/github/license/dbrattli/OSlash.svg)](https://github.com/dbrattli/OSlash/blob/master/LICENSE)

OSlash (Ø) is a library for learning and understanding functional programming in Python 3.12+. It re-implements
concepts from [Learn You a Haskell for Great Good!](http://learnyouahaskell.com/) using Python with modern type annotations. OSlash unifies
functional and object-oriented paradigms by grouping related functions within classes. Objects are never used
for storing values or mutable data; data exists only within function closures.

## ✨ What's New in 1.0

**OSlash 1.0 is a complete modernization** for Python 3.12+:

- **Modern Type System**: Fully type-checked with Pyright in strict mode
- **PEP 695 Syntax**: Clean type parameters (`class Maybe[T]:` instead of `Generic[T]`)
- **Modern Tooling**: Built with uv, formatted with ruff, validated with pre-commit hooks
- **Production Status**: Stable release ready for educational use

**Type Safety**: OSlash is fully type-checked with Pyright in strict mode, providing excellent IDE support and catching errors at development time. It leverages Python 3.12's PEP 695 type parameter syntax for clean, ergonomic generic types.

OSlash is intended to be a tutorial. For practical functional programming in Python in production environments you
should use [Expression](https://github.com/dbrattli/Expression) instead.

## Install

```bash
# Using pip
pip install oslash

# Or using uv (recommended)
uv add oslash
```

The project currently contains implementations for:

## Abstract Base Classes

- **[Functor](https://github.com/dbrattli/OSlash/wiki/Functors,-Applicatives,-And-Monads-In-Pictures#functors)**, for stuff that can be mapped
- **[Applicative](https://github.com/dbrattli/OSlash/wiki/Functors,-Applicatives,-And-Monads-In-Pictures#applicatives)**, for callable stuff
- **Monoid**, for associative stuff
- **[Monad](https://github.com/dbrattli/OSlash/wiki/Functors,-Applicatives,-And-Monads-In-Pictures#monads)**, for monadic stuff

## And Some Monads

- **Identity**, boxed stuff in its simplest form
- **[Maybe (Just | Nothing)](https://github.com/dbrattli/oslash/wiki/Functors,-Applicatives,-And-Monads-In-Pictures)**, for optional stuff
- **Either (Right | Left)**, for possible failures
- **List**, purely functional list of stuff
- **[IO Action](https://github.com/dbrattli/OSlash/wiki/Functors,-Applicatives,-And-Monads-In-Pictures#io-monad)**, for impure stuff
- **[Writer](https://github.com/dbrattli/OSlash/wiki/Three-Useful-Monads#the-writer-monad)**, for logging stuff
- **[Reader](https://github.com/dbrattli/OSlash/wiki/Three-Useful-Monads#the-reader-monad)**, for callable stuff
- **State**, for stateful computations of stuff
- **Cont**, for continuation of stuff

## Monadic functions

- **>>**, for sequencing monadic actions
- **lift**, for mapping a function over monadic values
- **join**, for removing one level of monadic structure
- **compose**, for composing monadic functions

## Utility functions

- **compose**, for composing 0 to n functions

## But why?

Yes, I know there are other projects out there like [PyMonad](https://bitbucket.org/jason_delaat/pymonad/),
[fn.py](https://github.com/kachayev/fn.py). I'm simply doing this in order to better understand the
[book](http://learnyouahaskell.com/). It's so much easier to learn when you implement things yourself. The code may be
similar to PyMonad in structure, but is quite different in implementation.

Why is the project called OSlash? OSlash is the Norwegian character called [Oslash](http://en.wikipedia.org/wiki/Ø).
Initially I wanted to create a project that used Ø and ø (unicode) for the project name and modules. It didn't work out
well, so I renamed it to OSlash.

## Examples

Haskell:

```haskell
> fmap (+3) (Just 2)
Just 5

> (+3) <$> (Just 2)
Just 5
```

Python:

```python
>>> Just(2).map(lambda x: x+3)
Just 5

>>> (lambda x: x+3) % Just(2)
Just 5

```

IO Actions:

```python
from oslash import put_line, get_line

main = put_line("What is your name?") | (lambda _:
    get_line() | (lambda name:
    put_line("What is your age?") | (lambda _:
    get_line() | (lambda age:
    put_line("Hello " + name + "!") | (lambda _:
    put_line("You are " + age + " years old"))))))

if __name__ == "__main__":
    main()
```

## Tutorials

- [Functors, Applicatives, And Monads In Pictures](https://github.com/dbrattli/oslash/wiki/Functors,-Applicatives,-And-Monads-In-Pictures) in Python.
- [Three Useful Monads](https://github.com/dbrattli/OSlash/wiki/Three-Useful-Monads) _(in progress)_
- [Using Either monad in Python](https://medium.com/@rnesytov/using-either-monad-in-python-b6eac698dff5)
