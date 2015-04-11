# Functors, Applicatives, And Monads in Python

Ø is a library for playing with functional programming in Python. It's
an attempt to re-implement some of the code from
[Learn You a Haskell for Great Good!](http://learnyouahaskell.com/) in
Python 3.4.

The project currently contains implementations for:

## Abstract Base Classes

 - **Functor**, for stuff that can be mapped
 - **Applicative**, for callable stuff
 - **Monoid**, for stuff that is associative
 - **Monad**, for monadic stuff

## And Some Monads

 - Identity
 - Maybe (Just | Nothing)
 - Either (Right | Left)
 - List
 - IO Action
 - Writer
 - Reader
 - State

## Monadic functions

- **>>**, for sequencing monadic actions
- **lift**, for mapping a function over a monadic value
- **join**, for removing one level of monadic structure
- **compose**, for composing monadic functions

## Utility functions

 - **compose**, for composing 0 to n functions

Yes, I know there are other projects out there like
[PyMonad](https://bitbucket.org/jason_delaat/pymonad/), but I'm simply doing
this in order to better understand the book. It's so much easier to learn when
you implement things yourself. The code may be similar to PyMonad in structure,
but is quite different in implementation.

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

* [Functors, Applicatives, And Monads In Pictures](https://github.com/dbrattli/oslash/wiki/Functors,-Applicatives,-And-Monads-In-Pictures) in Python.
* [Three Useful Monads](https://github.com/dbrattli/OSlash/wiki/Three-Useful-Monads) _(in progress)_
