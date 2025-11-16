# CLAUDE.md - OSlash Development Guide

## 📚 Project Overview

**OSlash** is an educational Python library that brings functional programming abstractions from Haskell to Python. With 740+ stars, it's used by developers learning functional programming concepts through practical Python implementations.

This project demonstrates:

- **Monadic composition** - Chain computations with context
- **Functors and Applicatives** - Map and apply operations
- **Protocol-based design** - Structural subtyping for flexibility
- **Modern Python 3.12+** - PEP 695 type parameters and match statements
- **Strict type safety** - Zero tolerance for type errors in CI

## 🎯 Philosophy

### Educational First

OSlash prioritizes learning and clarity over production concerns:

- **Explicit implementations** - Show how abstractions work, not just that they work
- **No backward compatibility constraints** - Always use latest Python features
- **Type safety as documentation** - Types teach correct usage patterns
- **Examples in code** - Tests and examples show idiomatic usage

### Functional Purity

Where practical, we maintain functional programming principles:

- **Immutability** - Data structures don't mutate
- **Referential transparency** - Functions return same output for same input
- **Composition over inheritance** - Build complex behavior from simple parts
- **Explicit effects** - IO monad makes side effects visible in types

### Modern Python

We embrace Python 3.12+ features aggressively:

- **PEP 695 type parameters** - `class Maybe[T]:` instead of `Generic[TypeVar]`
- **Pattern matching** - `match` statements for type discrimination
- **Type aliases** - `type Continuation[T, R] = Callable[[T], R]`
- **Protocol-based design** - Structural subtyping with `@runtime_checkable`

## 🏗️ Architecture

### Core Abstractions (Protocols)

Located in [oslash/typing/](oslash/typing/), these define the "laws" of functional programming:

#### 1. Functor - Mappable Containers

```python
@runtime_checkable
class Functor[T](Protocol):
    def map[U](self, fn: Callable[[T], U]) -> Functor[U]:
        """Transform values inside the container."""
        ...
```

**Law**: `functor.map(f).map(g) == functor.map(lambda x: g(f(x)))`

**Examples**: All monads are functors. Use `map` to transform wrapped values.

#### 2. Applicative - Apply Wrapped Functions

```python
@runtime_checkable
class Applicative[T](Protocol):
    def apply[U](self, something: Applicative[Callable[[T], U]]) -> Applicative[U]:
        """Apply a wrapped function to wrapped values."""
        ...

    @classmethod
    def pure(cls, value: T) -> Self:
        """Wrap a pure value."""
        ...
```

**Use case**: Lift functions of multiple arguments into the applicative context.

#### 3. Monad - Chainable Computations

```python
@runtime_checkable
class Monad[T](Protocol):
    def bind[U](self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        """Chain computations that produce wrapped values."""
        ...

    @classmethod
    def unit(cls, value: T) -> Self:
        """Wrap a pure value."""
        ...
```

**Law**: Left identity, right identity, associativity (see Haskell monad laws)

**Operators**:

- `|` for bind: `monad | func`
- `>>` for then: `monad1 >> monad2`

#### 4. Monoid - Combinable Values

```python
@runtime_checkable
class Monoid[T](Protocol):
    @classmethod
    def empty(cls) -> Self:
        """Identity element."""
        ...

    def __add__(self, other: Monoid[T]) -> Self:
        """Associative binary operation."""
        ...
```

**Laws**:

- Identity: `x + empty() == x` and `empty() + x == x`
- Associativity: `(x + y) + z == x + (y + z)`

### Monad Implementations

All located in [oslash/](oslash/):

#### 1. [Identity](oslash/identity.py) - Simplest Monad

```python
class Identity[T]:
    """Wraps a value with no additional context."""
```

**Use case**: Teaching monad laws, building monad transformers.

#### 2. [Maybe](oslash/maybe.py) - Optional Values

```python
class Maybe[T]:
    """Represents a computation that might fail."""

class Just[T](Maybe[T]):
    """Contains a value."""

class Nothing[T](Maybe[T]):
    """Represents absence of value."""
```

**Use case**: Handle null/None without explicit checks.

**Example**:

```python
def safe_div(x: float, y: float) -> Maybe[float]:
    if y == 0:
        return Nothing()
    return Just(x / y)

result = Just(10) | (lambda x: safe_div(x, 2)) | (lambda x: Just(x + 1))
# Result: Just(6.0)
```

#### 3. [Either](oslash/either.py) - Success or Failure

```python
class Either[T, E]:
    """Represents a computation that can fail with an error."""

class Right[T, E](Either[T, E]):
    """Success case."""

class Left[T, E](Either[T, E]):
    """Failure case with error information."""
```

**Use case**: Error handling with context about what went wrong.

**Example**:

```python
def parse_int(s: str) -> Either[int, str]:
    try:
        return Right(int(s))
    except ValueError:
        return Left(f"Cannot parse '{s}' as int")
```

#### 4. [List](oslash/list.py) - Immutable Linked List

```python
class List[T]:
    """Immutable list built from lambda expressions."""

class Cons[T](List[T]):
    """Non-empty list with head and tail."""

class Nil[T](List[T]):
    """Empty list."""
```

**Special feature**: Pure functional implementation using closures (Church encoding).

**Use case**: List comprehensions as monadic operations.

#### 5. [Reader](oslash/reader.py) - Environment Passing

```python
class Reader[Env, T]:
    """Passes shared environment through computation."""
```

**Use case**: Dependency injection, configuration passing.

#### 6. [Writer](oslash/writer.py) - Logging Computations

```python
class Writer[T, Log]:
    """Accumulates a log alongside computation."""
```

**Use case**: Collect diagnostic information without explicit parameters.

#### 7. [State](oslash/state.py) - Stateful Computations

```python
class State[T, S]:
    """Threads state through computation."""
```

**Use case**: Simulate mutable state functionally.

#### 8. [Cont](oslash/cont.py) - Continuations

```python
class Cont[T, R]:
    """Represents computation with explicit continuation."""

type Continuation[T, R] = Callable[[T], R]
```

**Use case**: Advanced control flow, implementing early returns.

#### 9. [IO](oslash/ioaction.py) - Side Effects

```python
class IO[T]:
    """Represents an effectful computation."""

class Return[T](IO[T]):
    """Pure value in IO context."""

class Put[T](IO[T]):
    """Print to stdout."""

class Get[T](IO[T]):
    """Read from stdin."""

class ReadFile(IO[str]):
    """Read file contents."""
```

**Use case**: Make side effects explicit in types. IO actions don't execute until `.run()` is called.

**Example**:

```python
program = (
    put_line("What's your name?") >>
    get_line() |
    (lambda name: put_line(f"Hello, {name}!"))
)
program.run(world=0)  # Execute the IO action
```

#### 10. [Observable](oslash/observable.py) - Reactive Streams

```python
class Observable[T]:
    """Represents a stream of values over time."""
```

**Use case**: Reactive programming patterns.

### Utility Functions

Located in [oslash/util/](oslash/util/):

#### [fn.py](oslash/util/fn.py) - Function Composition

```python
def compose[T](*funcs: Callable[[T], T]) -> Callable[[T], T]:
    """Compose functions right to left."""
    ...

identity: Callable[[T], T] = compose()

def fmap[T, U](func: Callable[[T], U], functor: Functor[T]) -> Functor[U]:
    """Flipped version of map for partial application."""
    return functor.map(func)
```

**Note**: Uses 7 `@overload` signatures to provide perfect type inference for 0-7 arguments.

#### [basic.py](oslash/util/basic.py) - Basic Utilities

```python
Unit: tuple[()] = ()  # Represents "no value" (like void)

def indent(level: int, size: int = 2) -> str:
    """Indent string by level."""
    ...
```

#### [numerals.py](oslash/util/numerals.py) - Church Encoding

```python
type ChurchBoolean[T] = Callable[[T], Callable[[T], T]]
type ChurchNumeral[T] = Callable[[Callable[[T], T]], Callable[[T], T]]

true: ChurchBoolean[T] = ...
false: ChurchBoolean[T] = ...
zero: ChurchNumeral[T] = ...
succ: Callable[[ChurchNumeral[T]], ChurchNumeral[T]] = ...
```

**Use case**: Educational - shows how to encode data as functions.

### [Kleisli Composition](oslash/monadic.py)

```python
def compose[A, B, C](
    f: Callable[[B], Monad[C]],
    g: Callable[[A], Monad[B]]
) -> Callable[[A], Monad[C]]:
    """Compose monadic functions."""
    return lambda x: g(x).bind(f)
```

**Use case**: Build pipelines of monadic operations.

## 🔧 Type System Patterns

### PEP 695 Type Parameters

**Always use PEP 695 syntax** introduced in Python 3.12:

```python
# ✅ GOOD - PEP 695
class Maybe[T]:
    def map[U](self, fn: Callable[[T], U]) -> Maybe[U]:
        ...

# ❌ BAD - Old style
from typing import Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')

class Maybe(Generic[T]):
    def map(self, fn: Callable[[T], U]) -> Maybe[U]:
        ...
```

**Benefits**:

- Cleaner syntax
- Scoped type parameters (no global TypeVar pollution)
- Better IDE support
- Signals modern Python 3.12+ codebase

### Type Aliases

Use `type` statement for complex types:

```python
# ✅ GOOD - PEP 695 type alias
type Continuation[T, R] = Callable[[T], R]
type ChurchNumeral[T] = Callable[[Callable[[T], T]], Callable[[T], T]]

# ❌ BAD - Old style
from typing import TypeAlias

Continuation: TypeAlias = Callable[[T], R]  # T, R must be defined elsewhere
```

### When `Any` is Acceptable

We minimize `Any` usage (<10 instances), but it's justified when:

1. **Higher-kinded types aren't supported**:

   ```python
   # List selector has dynamic return type based on runtime choice
   type ListSelector[T] = Callable[[T, List[T]], Any]  # Any: Return type varies
   ```

2. **Partial application creates ambiguity**:

   ```python
   # Partially applied function has complex intermediate type
   result = partial(func, arg1)  # type: ignore  # Partial: Complex type inference
   ```

3. **Protocol limitations**:

   ```python
   # Protocol can't express "returns same type as receiver"
   def copy(self) -> Any:  # Any: Protocol limitation, actual type is Self
   ```

**Always add inline comment** explaining why:

```python
value: Any  # Any: [Brief explanation of why static types insufficient]
```

### Self Type

Use `Self` for methods returning same type as receiver:

```python
from typing import Self

class Maybe[T]:
    @classmethod
    def empty(cls) -> Self:
        """Return Nothing of appropriate type."""
        return Nothing()

    def __add__(self, other: Self) -> Self:
        """Monoid combination."""
        ...
```

**Use cases**:

- Factory methods (`@classmethod`)
- Builder pattern methods
- Monoid operations
- Fluent interfaces

### Match Statements for Type Discrimination

Use `match` instead of `isinstance` chains for union types:

```python
# ✅ GOOD - Match statement
def __eq__(self, other: object) -> bool:
    match other:
        case Just(other_value):
            return self._value == other_value
        case Nothing():
            return False
        case _:
            return NotImplemented

# ❌ BAD - isinstance chain
def __eq__(self, other: object) -> bool:
    if isinstance(other, Just):
        return self._value == other._value
    elif isinstance(other, Nothing):
        return False
    else:
        return NotImplemented
```

**Benefits**:

- More concise
- Pattern matching shows intent
- Destructuring in patterns
- Exhaustiveness checking

### Variance

**Don't use variance annotations** with PEP 695 unless absolutely necessary:

```python
# ✅ GOOD - Simple, invariant
class Maybe[T]:
    ...

# ❌ AVOID - Rarely needed
class Maybe[T: covariant]:  # Only if you have a specific reason
    ...
```

**Reason**: Invariant types are simpler and sufficient for most use cases. Covariance/contravariance adds complexity.

## 🛠️ Development Workflow

### Setup

1. **Install dependencies**:

   ```bash
   uv sync --all-extras
   ```

2. **Install pre-commit hooks**:

   ```bash
   uv run pre-commit install
   ```

### Daily Workflow

1. **Before coding** - Check current state:

   ```bash
   uv run pyright
   uv run ruff check .
   ```

2. **While coding** - Fast feedback:

   ```bash
   # Format on save (configure your editor)
   # Or manually:
   uv run ruff format .

   # Check specific file:
   uv run pyright oslash/maybe.py
   ```

3. **Before committing** - Full validation:

   ```bash
   uv run pre-commit run --all-files
   ```

   This runs automatically on `git commit`, but running manually gives faster feedback.

4. **Run tests**:

   ```bash
   uv run pytest -v
   uv run pytest --cov=oslash --cov-report=term-missing
   ```

### Type Checking

**Strict mode is enabled** in pyproject.toml:

```toml
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
```

**Zero tolerance for type errors in CI**. Every type error must be fixed or suppressed with justification.

**Common type issues**:

1. **Missing return type**:

   ```python
   # ❌ BAD
   def foo():
       return 42

   # ✅ GOOD
   def foo() -> int:
       return 42
   ```

2. **Implicit Any**:

   ```python
   # ❌ BAD
   def process(items):  # items is implicitly Any
       ...

   # ✅ GOOD
   def process[T](items: list[T]) -> list[T]:
       ...
   ```

3. **Protocol implementation**:

   ```python
   # Ensure all protocol methods are implemented
   class MyMonad[T](Monad[T]):
       def bind[U](self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
           ...  # Must implement

       @classmethod
       def unit(cls, value: T) -> Self:
           ...  # Must implement
   ```

### Linting and Formatting

**ruff** handles both linting and formatting:

```bash
# Format code (modifies files)
uv run ruff format .

# Check for issues (doesn't modify)
uv run ruff check .

# Auto-fix issues (modifies files)
uv run ruff check . --fix
```

**Configuration** in pyproject.toml:

- Line length: 120
- Target: Python 3.12+
- Select: All recommended rules + many strict rules
- Ignore: Some stylistic rules that conflict with readability

### Testing

**pytest** with coverage:

```bash
# Run all tests
uv run pytest

# Verbose output
uv run pytest -v

# With coverage
uv run pytest --cov=oslash --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_maybe.py

# Run specific test
uv run pytest tests/test_maybe.py::test_just_map
```

**Test organization**:

- [tests/](tests/) - Unit tests for each monad
- Test file per module: `test_maybe.py`, `test_either.py`, etc.
- Use descriptive test names: `test_just_bind_chains_computations`

### Git Workflow

**Conventional commits** are required for release-please:

```bash
# Feature
git commit -m "feat: add alternative operator for monadic bind"

# Fix
git commit -m "fix: handle None in Maybe.map correctly"

# Docs
git commit -m "docs: add examples for Reader monad"

# Breaking change
git commit -m "feat!: require Python 3.12+

BREAKING CHANGE: Minimum Python version is now 3.12"
```

**Commit types**:

- `feat:` - New feature (minor version bump)
- `fix:` - Bug fix (patch version bump)
- `docs:` - Documentation only
- `refactor:` - Code change that neither fixes a bug nor adds a feature
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks
- `!` suffix or `BREAKING CHANGE:` - Major version bump

**Pre-commit hooks** run automatically:

- ruff format
- ruff check
- pyright
- trailing whitespace check
- end-of-file fixer

## 📝 Contribution Guidelines

### Adding a New Monad

1. **Create the module** in `oslash/your_monad.py`:

   ```python
   from __future__ import annotations

   from collections.abc import Callable
   from typing import TYPE_CHECKING

   from .typing import Functor, Monad

   if TYPE_CHECKING:
       pass


   class YourMonad[T]:
       """Docstring explaining what this monad represents."""

       def __init__(self, value: T) -> None:
           self._value = value

       @classmethod
       def unit(cls, value: T) -> YourMonad[T]:
           """Wrap a pure value."""
           return cls(value)

       def bind[U](self, func: Callable[[T], YourMonad[U]]) -> YourMonad[U]:
           """Monadic bind operation."""
           # Implementation depends on monad semantics
           return func(self._value)

       def map[U](self, func: Callable[[T], U]) -> YourMonad[U]:
           """Functor map operation."""
           return self.bind(lambda x: YourMonad.unit(func(x)))

       def __or__[U](self, func: Callable[[T], YourMonad[U]]) -> YourMonad[U]:
           """Use | as operator for bind."""
           return self.bind(func)

       def __rshift__[U](self, next: YourMonad[U]) -> YourMonad[U]:
           """The Then operator >> for sequencing."""
           return self.bind(lambda _: next)


   # Runtime protocol checks
   assert isinstance(YourMonad, Functor)
   assert isinstance(YourMonad, Monad)
   ```

2. **Add tests** in `tests/test_your_monad.py`:

   ```python
   from oslash.your_monad import YourMonad

   def test_your_monad_unit():
       """Test unit wraps value."""
       m = YourMonad.unit(42)
       assert m._value == 42

   def test_your_monad_bind():
       """Test bind chains computations."""
       m = YourMonad.unit(42)
       result = m.bind(lambda x: YourMonad.unit(x + 1))
       assert result._value == 43

   def test_your_monad_map():
       """Test map transforms value."""
       m = YourMonad.unit(42)
       result = m.map(lambda x: x * 2)
       assert result._value == 84

   def test_your_monad_left_identity():
       """unit(x).bind(f) == f(x)"""
       x = 42
       f = lambda a: YourMonad.unit(a + 1)
       assert YourMonad.unit(x).bind(f)._value == f(x)._value

   def test_your_monad_right_identity():
       """m.bind(unit) == m"""
       m = YourMonad.unit(42)
       assert m.bind(YourMonad.unit)._value == m._value

   def test_your_monad_associativity():
       """m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))"""
       m = YourMonad.unit(42)
       f = lambda x: YourMonad.unit(x + 1)
       g = lambda x: YourMonad.unit(x * 2)
       left = m.bind(f).bind(g)
       right = m.bind(lambda x: f(x).bind(g))
       assert left._value == right._value
   ```

3. **Export from oslash/**init**.py**:

   ```python
   from .your_monad import YourMonad

   __all__ = [
       ...,
       "YourMonad",
   ]
   ```

4. **Verify types**:

   ```bash
   uv run pyright oslash/your_monad.py
   ```

5. **Add documentation** (docstrings, examples, update README if public API)

### Code Style

1. **Always use `from __future__ import annotations`** at the top of every module
2. **PEP 695 type parameters** for all generics
3. **Import from `collections.abc`** instead of `typing` when possible:

   ```python
   from collections.abc import Callable, Iterable  # ✅ GOOD
   from typing import Callable, Iterable  # ❌ AVOID (works but less modern)
   ```

4. **Use `TYPE_CHECKING`** for imports only needed for type hints:

   ```python
   from typing import TYPE_CHECKING

   if TYPE_CHECKING:
       from .other_module import SomeType
   ```

5. **Match statements** over isinstance chains for type discrimination
6. **Explicit return types** on all functions (strict mode requirement)
7. **Docstrings** on all public classes and functions

### Testing Requirements

1. **Test all public methods**
2. **Test monad laws** (left identity, right identity, associativity)
3. **Test protocol conformance** (include runtime checks with `assert isinstance`)
4. **Test edge cases** (empty, None, errors)
5. **Use descriptive test names** that explain what's being tested
6. **Coverage >80%** (aim for >90%)

### Documentation Requirements

1. **Module docstring** at top of file
2. **Class docstring** explaining what the class represents
3. **Method docstrings** for public methods (can be brief for obvious methods)
4. **Examples** in docstrings using doctest format when helpful
5. **Type hints** are part of documentation - make them precise

## 🎓 Why Protocols Over Abstract Base Classes?

OSlash uses **Protocol** instead of **ABC** for type definitions. Here's why:

### Structural vs Nominal Typing

**Protocol** (structural typing):

```python
@runtime_checkable
class Functor[T](Protocol):
    def map[U](self, fn: Callable[[T], U]) -> Functor[U]: ...

# Any class with a map method is a Functor - no inheritance needed
class MyClass[T]:
    def map[U](self, fn: Callable[[T], U]) -> MyClass[U]:
        ...

assert isinstance(MyClass, Functor)  # ✅ True!
```

**ABC** (nominal typing):

```python
class Functor[T](ABC):
    @abstractmethod
    def map[U](self, fn: Callable[[T], U]) -> Functor[U]: ...

# Must explicitly inherit
class MyClass[T](Functor[T]):  # ❌ Required!
    def map[U](self, fn: Callable[[T], U]) -> MyClass[U]:
        ...
```

### Benefits for OSlash

1. **Educational clarity**: Shows that Functor/Monad/etc are *interfaces*, not implementation details
2. **Less coupling**: Implementations don't need to know about protocols
3. **Multiple protocols**: A class can satisfy multiple protocols without multiple inheritance complexity
4. **Duck typing**: "If it has a map method, it's a Functor" - very Pythonic
5. **Runtime checks**: `@runtime_checkable` allows `isinstance(obj, Protocol)` checks

### When to Use ABC

Use ABC when you:

- Want to share implementation code (mixin methods)
- Need enforced method signatures at definition time
- Want to prevent instantiation of base class
- Have a strict inheritance hierarchy

OSlash doesn't need these - protocols are sufficient.

## 🔗 References and Resources

### Functional Programming

- [Learn You a Haskell](http://learnyouahaskell.com/) - Excellent Haskell tutorial
- [Haskell Wiki: Monad laws](https://wiki.haskell.org/Monad_laws)
- [Functors, Applicatives, And Monads In Pictures](https://adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html)

### Python Type System

- [PEP 695 – Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [PEP 544 – Protocols](https://peps.python.org/pep-0544/)
- [Pyright Documentation](https://microsoft.github.io/pyright/)
- [typing module docs](https://docs.python.org/3/library/typing.html)

### Project Tools

- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [ruff](https://github.com/astral-sh/ruff) - Fast Python linter
- [release-please](https://github.com/googleapis/release-please) - Automated versioning

### Similar Projects

- [returns](https://github.com/dry-python/returns) - Production-ready monads for Python
- [PyMonad](https://github.com/jasondelaat/pymonad) - Another educational monad library
- [toolz](https://github.com/pytoolz/toolz) - Functional utilities for Python

## 🚀 Quick Start for Contributors

```bash
# Clone and setup
git clone https://github.com/dbrattli/OSlash.git
cd OSlash
uv sync --all-extras
uv run pre-commit install

# Make changes
# ... edit code ...

# Validate before committing
uv run ruff format .
uv run ruff check . --fix
uv run pyright
uv run pytest -v

# Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: your change description"

# Push (CI will run)
git push
```

## 💡 Tips for Working with Monads

### Bind vs Map

- **Use `map`** when your function returns a plain value: `maybe.map(lambda x: x + 1)`
- **Use `bind`** when your function returns a monad: `maybe.bind(lambda x: safe_div(x, 2))`

### The Pipe Operator

Use `|` for readable chains:

```python
result = (
    Just(10)
    | (lambda x: safe_div(x, 2))
    | (lambda x: Just(x + 1))
    | (lambda x: Just(x * 2))
)
```

### The Then Operator

Use `>>` to sequence actions, ignoring intermediate results:

```python
program = (
    put_line("Starting...")
    >> put_line("Processing...")
    >> put_line("Done!")
)
```

### When to Use Which Monad

- **Maybe**: Computations that might fail (divide by zero, missing dict key)
- **Either**: Computations that fail with error information (parsing, validation)
- **List**: Non-deterministic computations (all possible outcomes)
- **Reader**: Pass configuration/environment through computation
- **Writer**: Collect logs/diagnostics alongside result
- **State**: Thread mutable state through pure functions
- **IO**: Represent side effects without performing them
- **Cont**: Advanced control flow, early returns, coroutines
- **Observable**: Streams of values over time (reactive programming)

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/dbrattli/OSlash/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dbrattli/OSlash/discussions)
- **Type errors**: Check pyright output, review this guide's type system section
- **Monad laws**: See Haskell Wiki or "Learn You a Haskell"

## ✨ Credits

**OSlash** was created by Dag Brattli as an educational project to learn Haskell by reimplementing its abstractions in Python.

Modernized in 2025 to Python 3.12+ with PEP 695 type parameters, strict type checking, and modern tooling.

**Contributors**: See [GitHub contributors](https://github.com/dbrattli/OSlash/graphs/contributors)

---

*Happy functional programming! 🎉*
