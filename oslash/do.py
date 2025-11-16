#!/usr/bin/env python3
"""Monadic do notation for Python."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, NamedTuple

from .typing import Monad
from .util import Unit

# This would be most natural to implement as a syntactic macro.
# But to stay within Python's builtin capabilities, this is a code generator.
#
# The price is the sprinkling of "lambda e: ..."s to feed in the environment,
# and manually simulated lexical scoping for env attrs instead of just
# borrowing Python's for run-of-the-mill names.


# TODO: guard belongs where in OSlash?
def guard[T](m: Monad[T], test: bool) -> Monad[tuple[()]]:
    """Monadic guard.

    What it does::

        return M.pure(Unit) if test else M.empty()

    https://en.wikibooks.org/wiki/Haskell/Alternative_and_MonadPlus#guard
    """
    return m.pure(Unit) if test else m.empty()  # type: ignore[return-value,attr-defined]


# The kwargs syntax forces name to be a valid Python identifier.
class MonadicLet(NamedTuple):
    """Represents a monadic let binding."""

    name: str
    value: Any  # Any: Can be Monad or Callable returning Monad


def let(**binding: Any) -> MonadicLet | None:  # Any: Dynamic binding value
    """``<-`` for Python.

    Haskell::

        a <- [1, 2, 3]

    Python::

        let(a=List.from_iterable((1, 2, 3)))
    """
    if len(binding) != 1:
        raise ValueError(f"Expected exactly one binding, got {len(binding):d} with values {binding}")
    for k, v in binding.items():
        return MonadicLet(k, v)
    return None


def do(*lines: Monad[Any] | MonadicLet | Callable[[Any], Monad[Any]]) -> Monad[Any]:
    """Do-notation.

    Syntax::

        do(line,
           ...)

    where each ``line`` is one of::

        let(name=body)   # Haskell:  name <- expr (see below on expr)
        body             # Haskell:  expr

    where ``name`` is a Python identifier.

      - Use ``let(name=body)`` when you want to bind a name to the extracted value,
        for use on any following lines.

      - Use only ``body`` when you just want to sequence operations,
        and on the last line.

    Here ``body`` is one of:

      - An expression ``expr`` that evaluates to a Monad instance.

      - A one-argument function which takes in the environment, such as
        ``lambda e: expr``, and when called (with the environment as its
        only argument), returns a Monad instance. This allows accessing
        the ``let`` bindings in the environment.

    **Examples**. This Haskell::

        do
          a <- [3, 10, 6]
          b <- [100, 200]
          return a + b

    pythonifies as::

        l = lambda *items: List.from_iterable(items)
        do(let(a=l(3, 10, 6)),      # e.a <- ...
           let(b=l(100, 200)),      # e.b <- ...
           lambda e: List.unit(e.a + e.b))  # access the env via lambda e: ...

    which has the same effect as::

        l(3, 10, 6) | (lambda a:
        l(100, 200) | (lambda b:
        List.unit(a + b)))

    *Pythagorean triples*. (A classic test case for McCarthy's *amb* operator.)

    Denote ``z`` = hypotenuse, ``x`` = shorter leg, ``y`` = longer leg,
    so their lengths ``z >= y >= x``. Define::

        def r(low, high):
            return List.from_iterable(range(low, high))

    Now::

        pt = do(let(z=r(1, 21)),
                let(x=lambda e: r(1, e.z+1)),  # needs the env to access "z"
                let(y=lambda e: r(e.x, e.z+1)),
                lambda e: guard(List, e.x*e.x + e.y*e.y == e.z*e.z),
                lambda e: List.unit((e.x, e.y, e.z)))

    which has the same effect as::

        pt = r(1, 21)  | (lambda z:
             r(1, z+1) | (lambda x:
             r(x, z+1) | (lambda y:
             guard(List, x*x + y*y == z*z) >>
             List.unit((x,y,z)))))
    """
    # The monadic bind and sequence operators, with any relevant whitespace.
    bind = " | "
    seq = " >> "

    class Env:
        def __init__(self) -> None:
            self.names: set[str] = set()

        def assign(self, k: str, v: Any) -> None:  # Any: Dynamic attribute values
            self.names.add(k)
            setattr(self, k, v)

        # simulate lexical closure property for env attrs
        #   - free_vars: set of names that "fall in" from a surrounding lexical scope
        def close_over(self, free_vars: set[str]) -> None:
            names_to_clear = {k for k in self.names if k not in free_vars}
            for k in names_to_clear:
                delattr(self, k)
            self.names = free_vars.copy()

    # stuff used inside the eval
    e = Env()

    def begin(*exprs: Any) -> Any:  # Any: args eagerly evaluated by Python
        # begin(e1, e2, ..., en):
        #   perform side effects e1, e2, ..., e[n-1], return the value of en.
        return exprs[-1]

    all_code = ""
    names: set[str] = set()  # names seen so far (working line by line, so textually!)
    bodies: list[Any] = []  # Any: Can be Monad or Callable
    begin_is_open = False
    for j, item in enumerate(lines):
        is_first = j == 0
        is_last = j == len(lines) - 1

        name: str | None
        body: Any  # Any: Can be Monad or Callable
        if isinstance(item, MonadicLet):
            name, body = item
        else:
            name, body = None, item
        bodies.append(body)

        free_vars: set[str] = names.copy()  # names from the surrounding scopes
        if name:
            names.add(name)

        code: str
        if isinstance(body, Monad):  # doesn't need the environment
            code = f"bodies[{j:d}]"
        elif callable(body):  # lambda e: ...
            # TODO: check arity (see unpythonic.arity.arity_includes)
            code = f"bodies[{j:d}](e)"
        else:
            raise TypeError(f"Unexpected body type '{type(body)}' with value '{body}'")

        if begin_is_open:
            code += ")"
            begin_is_open = False

        # monadic-bind or sequence to the next item, leaving only the appropriate
        # names defined in the env (so that we get proper lexical scoping
        # even though we use an imperative stateful object to implement it)
        if not is_last:
            if name:
                code += f"{bind:s}(lambda {name:s}:\nbegin(e.close_over({free_vars}), e.assign('{name:s}', {name:s}), "
                begin_is_open = True
            elif is_first:
                code += f"{bind:s}(lambda _:\nbegin(e.close_over(set()), "
                begin_is_open = True
            else:
                code += f"{seq:s}(\n"

        all_code += code
    all_code += ")" * (len(lines) - 1)

    # The eval'd code doesn't close over the current lexical scope,
    # so provide the necessary names as its globals.
    return eval(all_code, {"e": e, "bodies": bodies, "begin": begin})


__all__ = ["do", "guard", "let"]
