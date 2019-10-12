# Functors, Applicatives, And Monads in Python

Ø is a library for playing with functional programming in Python. It's
an attempt to re-implement some of the code from
[Learn You a Haskell for Great Good!](http://learnyouahaskell.com/) in
Python 3.4. Ø unifies functional and object oriented paradigms by
grouping related functions within classes. Objects are however never
used for storing values or mutable data, and data only lives within
function closures.

## Install

```bash
> pip3 install oslash
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

Yes, I know there are other projects out there like
[PyMonad](https://bitbucket.org/jason_delaat/pymonad/),
[fn.py](https://github.com/kachayev/fn.py). I'm simply doing this in order to
better understand the book. It's so much easier to learn when you implement
things yourself. The code may be similar to PyMonad in structure, but is
quite different in implementation.

Why is the project called OSlash? OSlash is the Norwegian character called
[Oslash](http://en.wikipedia.org/wiki/Ø). Initially I wanted to create a
project that used Ø and ø (unicode) for the project name and modules. It didn't
work out well, so I renamed it to Oslash.

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
