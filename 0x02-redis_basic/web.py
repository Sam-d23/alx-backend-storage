#!/usr/bin/env python3
"""
Module for fetching web pages and caching their content using Redis.
"""


import requests
import redis
import time
from typing import Callable


# Initialize Redis connection
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL and
    caches it with a 10-second expiration.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content of the web page.
    """
    # Check Redis cache first
    cached_content = redis_conn.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    # Fetch HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the fetched content with a 10-second expiration
    redis_conn.setex(url, 10, html_content)

    # Track the number of accesses for this URL
    redis_conn.incr(f"count:{url}")

    return html_content

def cache_page_expiration(seconds: int) -> Callable:
    """
    Decorator to cache the return value of a
    function with a specified expiration time.

    Args:
        seconds (int): The expiration time in seconds.

    Returns:
        Callable: Decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            cached_content = redis_conn.get(url)
            if cached_content:
                return cached_content.decode('utf-8')

            result = func(*args, **kwargs)
            redis_conn.setex(url, seconds, result)
            redis_conn.incr(f"count:{url}")

            return result
        return wrapper
    return decorator

# Example usage of the decorator for get_page function
@cache_page_expiration(seconds=10)
def get_page_with_caching(url: str) -> str:
    """
    Fetches the HTML content of a given URL
    and caches it with a specified expiration time.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content of the web page.
    """
    response = requests.get(url)
    return response.text
