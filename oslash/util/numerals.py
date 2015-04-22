"""
Lambda calculus.

* http://en.wikipedia.org/wiki/Church_encoding
* http://www.cs.bham.ac.uk/~axj/pub/papers/lambda-calculus.pdf
* http://vanderwijk.info/blog/pure-lambda-calculus-python/
* http://eflorenzano.com/blog/2008/11/20/lambda-calculus/

Just for the fun of it.
"""


identity = lambda x: x
self_apply = lambda s: s(s)

select_first = lambda first: lambda second: first
select_second = lambda first: lambda second: second

make_pair = lambda first: lambda second: lambda func: func(first)(second)

apply = lambda func: lambda arg: func(arg)

cond = lambda e1: lambda e2: lambda c: c(e1)(e2)

true = select_first
false = select_second

iff = lambda c, a, b: c(a)(b)

not_ = lambda x: cond(false)(true)(x)
and_ = lambda x: lambda y: x(y)(false)
or_ = lambda x: lambda y: x(true)(y)

# succ = λn.λf.λx.f (n f x)
succ = lambda n: lambda f: lambda x: f(n(f)(x))

zero = lambda f: identity
one = lambda f: lambda x: f(x)

two = succ(one)
three = succ(two)

iszero = lambda n: n(select_first)

to_int = lambda n: n(lambda x: x + 1)(0)
printl = lambda n: n(lambda x: x + 1)(0)
