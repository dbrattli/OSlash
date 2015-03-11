# Ø (Oslash) - Functors, Applicatives, And Monads in Python

Ø is an attempt to re-implement some of the code from 
[Learn You a Haskell for Great Good!](http://learnyouahaskell.com/) in
Python 3.4. The project currently contains implementations for:

## Abstract Base Classes

 - Functor
 - Applicative
 - Monoid
 - Monad

## And Some Monads
 
 - Maybe (Just | Nothing)
 - Either (Right | Left)
 - List
 - IOAction

Yes, I know there are other projects out there like 
[PyMonad](https://bitbucket.org/jason_delaat/pymonad/), but I'm simply doing 
this in order to better understand the book. It's so much easier to learn when 
you implement things yourself. The code may be similar to PyMonad in structure, 
but is quite different in implementation.

Why is the project called Ø? Ø is the Norwegian character called 
[Oslash](http://en.wikipedia.org/wiki/Ø). Just want to check if it's possible 
to have a projects name that uses unicode characters. 
Q: How do I write an ø on an american or english keybord?
A: Are you really sure you want to understand Monads? Copy/paste?

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
>>> Just(2).fmap(lambda x: x+3)
Just 5

>>> (lambda x: x+3) % Just(2)
Just 5

```

## Tutorial

You might already have checked out the excellent [Functors, Applicatives, And Monads In Pictures](adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html).

How would that look if we translated it to Python? Well, here is
[Functors, Applicatives, And Monads In Pictures](https://github.com/dbrattli/oslash/wiki/Functors,-Applicatives,-And-Monads-In-Pictures) in Python.
