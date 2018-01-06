from oslash import List

IntList = List[int]


def f() -> IntList:
    """Return list.."""
    return List.unit(0)
