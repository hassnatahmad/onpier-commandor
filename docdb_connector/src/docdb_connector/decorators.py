import inspect
import logging
import time
from functools import wraps
from typing import Any, List

log = logging.getLogger(__name__)


def fullname(o):
    module = inspect.getmodule(o)
    return f"{module.__name__}.{o.__qualname__}"


def scheduled_project_task(func):
    """Decorator that sets up a background task function with
    a database session and exception tracking.

    Each task is executed in a specific project context.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
        elapsed_time = time.perf_counter() - start

    return wrapper


def background_task(func):
    """Decorator that sets up the a background task function
    with a database session and exception tracking.

    As background tasks run in their own threads, it does not attempt
    to propagate errors.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_time = time.perf_counter() - start
            return result
        except Exception as e:
            log.exception(e)

    return wrapper


def timer(func: Any):
    """Timing decorator that sends a timing metric."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start
        log.debug(f"function.elapsed.time.{fullname(func)}: {elapsed_time}")
        return result

    return wrapper


def counter(func: Any):
    """Counting decorator that sends a counting metric."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def apply(decorator: Any, exclude: List[str] = None):
    """Class decorator that applies specified decorator to all class methods."""
    if not exclude:
        exclude = []

    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and attr not in exclude:
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate
