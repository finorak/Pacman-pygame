import sys
from collections.abc import Callable
from functools import wraps
from typing import Any

from pydantic import ValidationError


def log(msg: Any) -> None:
    print(msg, file=sys.stderr)


def error_handler(func: Callable[..., None]) -> Callable:
    @wraps(func)
    def wrapper(*arg: Any, **kwarg: Any) -> Any:
        try:
            return func(*arg, **kwarg)
        except FileNotFoundError as e:
            log(e)
        except ValidationError as e:
            msg = e.errors()[0]["msg"]
            log(msg)
        except PermissionError as e:
            log(e)
        except Exception as e:
            log(e)

    return wrapper
