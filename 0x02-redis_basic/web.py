#!/usr/bin/env python3
"""
Caches HTTP requests and tracking access.
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Initializing a Redis client
redis_client = redis.Redis()


def track_get_page(fn: Callable) -> Callable:
    """
    Decorator of get_page that caches and tracks access.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        Wrapper which increments access count and caches data.
        """
        redis_client.incr(f'count:{url}')
        cached_page = redis_client.get(url)
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        redis_client.setex(url, 10, response)
        return response

    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    A HTTP GET request is made and returns the response text.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text
