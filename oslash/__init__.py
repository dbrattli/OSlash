"""OSlash - Functional programming in Python.

A Python library for functional programming with monads, functors, and applicatives.
"""

from __future__ import annotations

# Monads
from .cont import Cont
from .do import do, guard, let
from .either import Either, Left, Right
from .identity import Identity
from .ioaction import IO, Get, Put, ReadFile, Return, get_line, put_line, read_file
from .list import List
from .maybe import Just, Maybe, Nothing

# Utilities
from .monadic import compose as monadic_compose
from .observable import Observable
from .reader import MonadReader, Reader
from .state import State

# Protocols
from .typing import Applicative, Functor, Monad, Monoid
from .util import Unit, compose, fmap, identity, indent
from .writer import MonadWriter, StringWriter, Writer

# Version will be managed by release-please
__version__ = "0.7.0"

__all__ = [
    "IO",
    "Applicative",
    "Cont",
    "Either",
    "Functor",
    "Get",
    "Identity",
    "Just",
    "Left",
    "List",
    "Maybe",
    "Monad",
    "MonadReader",
    "MonadWriter",
    "Monoid",
    "Nothing",
    "Observable",
    "Put",
    "ReadFile",
    "Reader",
    "Return",
    "Right",
    "State",
    "StringWriter",
    "Unit",
    "Writer",
    "compose",
    "do",
    "fmap",
    "get_line",
    "guard",
    "identity",
    "indent",
    "let",
    "monadic_compose",
    "put_line",
    "read_file",
]
