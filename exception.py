from typing import Any
from abc import ABC, abstractmethod


class ErrorABC(Exception, ABC):
    """Abstrac class for an errror."""

    def __init__(self, *args: Any, **kwargs: object):
        self.message = self.generate_error_msg(*args, **kwargs)
        super().__init__(self.message)

    @staticmethod
    @abstractmethod
    def generate_error_msg(args: Any, **kwargs: object) -> str:
        pass

    def __str__(self) -> str:
        return self.message
