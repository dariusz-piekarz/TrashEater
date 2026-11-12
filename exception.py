from typing import Any
from abc import ABC, abstractmethod


class ErrorABC(Exception, ABC):
    """Abstrac class for an errror."""

    def __init__(self, *args: Any, **kwargs: object):
        """Initialize the exception using its subclass-generated message.

        Parameters
        ----------
        *args : Any
            Positional values forwarded to :meth:`generate_error_msg`.
        **kwargs : object
            Keyword values forwarded to :meth:`generate_error_msg`.
        """
        self.message = self.generate_error_msg(*args, **kwargs)
        super().__init__(self.message)

    @staticmethod
    @abstractmethod
    def generate_error_msg(args: Any, **kwargs: object) -> str:
        """Generate the message used to initialize the exception.

        Parameters
        ----------
        args : Any
            Positional value supplied by the subclass's exception
            initialization.
        **kwargs : object
            Additional values supplied by the subclass.

        Returns
        -------
        str
            Human-readable exception message.
        """
        pass

    def __str__(self) -> str:
        """Return the generated exception message.

        Returns
        -------
        str
            Human-readable exception message.
        """
        return self.message
