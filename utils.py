"""Bad style, but I don't know better where to put this."""

import logging
import shelve
from functools import wraps

logger = logging.getLogger(__name__)

def shelve_memoize(filename):
    """On-disk cache decorator using shelve."""
    def decorator_shelve_memoize(func):
        @wraps(func)
        def wrapper_shelve_memoize(arxiv_id, *args, **kwargs):
            assert len(args) == 0
            assert len(kwargs) == 0
            with shelve.open(filename) as db: # noqa: S301
                if arxiv_id not in db:
                    logger.debug(f"{arxiv_id} was not found in the local metadata db. Requesting…")
                    db[arxiv_id] = func(arxiv_id)
                return db.get(arxiv_id)
    return decorator_shelve_memoize
