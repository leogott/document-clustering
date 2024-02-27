"""Miscellaneous functions that would be lonely in their seperate files.

Bad style, I know, but I made up for it in documentation!
"""


import logging
import shelve
from collections.abc import Callable
from contextlib import contextmanager
from functools import wraps
from time import perf_counter_ns
from typing import Any

logger = logging.getLogger(__name__)

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

## Memoize

def shelve_memoize(filename: str):
    """On-disk cache decorator using shelve."""
    def decorator_shelve_memoize(func: Callable[[str], Any]):
        @wraps(func)
        def wrapper_shelve_memoize(arxiv_id):
            with shelve.open(filename) as db: # noqa: S301
                if arxiv_id not in db:
                    logger.debug(f"{arxiv_id} was not found in the local metadata db. Requesting…")
                    db[arxiv_id] = func(arxiv_id)
                return db.get(arxiv_id)
        return wrapper_shelve_memoize
    return decorator_shelve_memoize

def shelve_forget(filename: str, arxiv_id):
    """Clear a specific item from the shelve."""
    with shelve.open(filename) as db: # noqa: S301
        del db[arxiv_id]

## Track execution time

@contextmanager
def execution_time():
    """Log the runtime of the decorated function."""
    t0 = t1 = perf_counter_ns()
    def get_time_delta():
        return t1-t0
    yield get_time_delta
    t1 = perf_counter_ns()
