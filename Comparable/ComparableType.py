from abc import ABCMeta, abstractmethod
from typing import Protocol


class ComparableType(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, __value: object, /) -> bool: ...
