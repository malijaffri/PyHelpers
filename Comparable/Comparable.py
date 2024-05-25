from typing import Callable, Self
from .ComparableType import ComparableType as CT


class Comparable:
    """Implements logical operators for subclasses.

    Uses one attribute as basis for comparison.
    If the specified method does not exist for the attribute, it is simulated based on __lt__.
    We assume that __lt__ exists, because the standard library does the same.
    """

    __slots__ = "__comparable_attr"

    def __init__(self, attr: str) -> None:
        """Initialises the attribute which stores this class's comparable attribute.

        Args:
            attr (str): the name of the attribute to compare.
        """
        self.__comparable_attr: str = attr

    def __get__comparable_attr(self) -> CT:
        return getattr(self, self.__comparable_attr)

    @staticmethod
    def __comparable_helper(__own: CT, __other: CT, __attr: str, __default: bool) -> bool:
        func: Callable[[CT, CT], bool] | None = getattr(type(__own), __attr, None)
        if callable(func) and func is not getattr(object, __attr, None):
            return func(__own, __other)
        else:
            return __default

    def __lt__(self, __value: Self, /) -> bool:
        """lesser than"""
        own: CT = self.__get__comparable_attr()
        other: CT = __value.__get__comparable_attr()
        return own < other

    def __gt__(self, __value: Self, /) -> bool:
        """greater than"""
        own: CT = self.__get__comparable_attr()
        other: CT = __value.__get__comparable_attr()
        return self.__comparable_helper(own, other, "__gt__", other < own)

    def __eq__(self, __value: Self, /) -> bool:
        """equal"""
        own: CT = self.__get__comparable_attr()
        other: CT = __value.__get__comparable_attr()
        return self.__comparable_helper(own, other, "__eq__", not ((own < other) or (other < own)))

    def __ge__(self, __value: Self, /) -> bool:
        """greater or equal"""
        own: CT = self.__get__comparable_attr()
        other: CT = __value.__get__comparable_attr()
        return self.__comparable_helper(own, other, "__ge__", not (own < other))

    def __le__(self, __value: Self, /) -> bool:
        """lesser or equal"""
        own: CT = self.__get__comparable_attr()
        other: CT = __value.__get__comparable_attr()
        return self.__comparable_helper(own, other, "__le__", not (other < own))

    def __ne__(self, __value: Self, /) -> bool:
        """not equal"""
        own: CT = self.__get__comparable_attr()
        other: CT = __value.__get__comparable_attr()
        return self.__comparable_helper(own, other, "__ne__", (own < other) or (other < own))
