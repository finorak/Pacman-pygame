"""Error handler module."""

import sys
from collections.abc import Callable
from functools import wraps
from typing import Any

from pydantic import ValidationError


def _log(msg: Any) -> None:
    print(msg, file=sys.stderr)


def error_handler(func: Callable[..., None]) -> Callable:
    """Handle error gracefully.

    Instead of checking manually every error in our code
    we just wrapp the main function with this one
    so that our code is more readable and can focus
    on implementing other than checking error possible
    every time.

    Args:
        func: The function we want to wrap
    Returns:
        wrapper: the wrapper function to wrap our functin.
    """
    @wraps(func)
    def wrapper(*arg: Any, **kwarg: Any) -> Any:
        """Wrap function."""
        try:
            return func(*arg, **kwarg)
        except FileNotFoundError as e:
            _log(e)
        except ValidationError as e:
            msg = e.errors()[0]["msg"]
            _log(msg)
        except PermissionError as e:
            _log(e)
        except Exception as e:
            _log(e)

    return wrapper
