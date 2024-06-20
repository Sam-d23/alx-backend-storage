#!/usr/bin/env python3
"""
Module caches HTTP requests and tracks access.
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Redis client is initialized
redis_client = redis.Redis()


def track_get_page(fn: Callable) -> Callable:
    """
    Decorator checks if URL's data is cached
    and tracks number of times get_page is called
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        Increments access count for the URL
        and returns available cached data.
        Fetches and caches data if not available
        """
        # Number of times the URL is accessed, is tracked
        redis_client.incr(f'count:{url}')
        # Check whether URL's data is cached
        cached_page = redis_client.get(url)
        if cached_page:
            return cached_page.decode('utf-8')
        # Fetches data and cache it
        response = fn(url)
        redis_client.setex(url, 10, response)
        return response

    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    HTTP GET request to a given URL is made
    and the response text is returned.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text
