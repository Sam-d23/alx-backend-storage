#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''

import redis
import requests
from functools import wraps
from typing import Callable


redis = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """Wrapper Decorator"""

    @wraps(fn)
    def wrapper(url):
        """ Wrapper decorator"""
        redis.incr(f"count:{url}")
        cached_response = redis.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        result = fn(url)
        redis.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.'''
    return requests.get(url).text
