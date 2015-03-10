# A Project Called Ø (Oslash)

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

Yes, I know there are other projects out there like 
[PyMonad](https://bitbucket.org/jason_delaat/pymonad/), but I'm simply doing 
this in order to better understand the book. It's so much easier to learn when 
you implement things yourself. The code may be similar to PyMonad in structure, 
but is quite different in implementation.

Why is the project called Ø? Ø is the Norwegian character called 
[Oslash](http://en.wikipedia.org/wiki/Ø). Just want to check if it's possible 
to have a projects name that uses unicode characters.

## Examples

```haskell
> fmap (+3) (Just 2)
Just 5
```

```python
>>> Just(2).fmap(lambda x: x+3)
Just 5
```
