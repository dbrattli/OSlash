from typing import Callable, List, TypeVar, Union

T = TypeVar('T')      # Declare type variable


def extensionmethod(base: T, name=None, decorator: Callable=None,
                    alias: Union[str, List[str]]=None) -> Callable:
    """Function decorator that extends base with the decorated function.

    Keyword arguments:
    :param T base: Base class to extend with method
    :param string name: Name of method to set

    :returns: A function that takes the class to be decorated.
    :rtype: func -> func
    """
    def inner(func: Callable):
        """This function is returned by the outer extensionmethod()"""

        func_names = [name or func.__name__]
        if alias:
            aliases = alias if isinstance(alias, list) else [alias]
            func_names += aliases

        func = decorator(func) if decorator else func

        for func_name in func_names:
            setattr(base, func_name, func)
        return func
    return inner


def extensionclassmethod(base: T, name: str=None,
                         alias: Union[str, List[str]]=None) -> Callable:
    """Function decorator that extends base with the decorated
    function as a class method.

    Keyword arguments:
    :param T base: Base class to extend with classmethod
    :param string name: Name of method to set

    :returns: A function that takes the class to be decorated.
    :rtype: func -> func
    """

    return extensionmethod(base=base, name=name, decorator=classmethod, alias=alias)
