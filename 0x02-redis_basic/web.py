#!/usr/bin/env python3
"""
Module for fetching web pages with caching and counting.
"""


import requests
import redis
from typing import Callable
from functools import wraps
from time import sleep


redis_client = redis.Redis(host='localhost', port=6379, db=0)


def cache_and_count(func: Callable) -> Callable:
    """
    Decorator to cache function results
    in Redis with a count of accesses.

    Args:
        func (Callable): Function to decorate.

    Returns:
        Callable: Decorated function.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Wrapper function to cache and count
        accesses for the decorated function.

        Args:
            url (str): URL of the web page to fetch.

        Returns:
            str: HTML content of the web page.
        """
        # Count accesses
        count_key = f"count:{url}"
        redis_client.incr(count_key)

        # Cache result with expiration time
        content_key = f"content:{url}"
        cached_content = redis_client.get(content_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # Fetch content if not cached
        html_content = func(url)
        redis_client.setex(content_key, 10, html_content)

        return html_content

    return wrapper


@cache_and_count
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a web page.

    Args:
        url (str): URL of the web page to fetch.

    Returns:
        str: HTML content of the web page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""
