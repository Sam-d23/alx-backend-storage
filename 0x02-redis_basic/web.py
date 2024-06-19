#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.'''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''Wrapper function for caching the output.'''
        key_count = f'count:{url}'
        key_result = f'result:{url}'

        redis_store.incr(key_count)
        cached_result = redis_store.get(key_result)
        if cached_result:
            return cached_result.decode('utf-8')

        result = method(url)
        redis_store.setex(key_result, 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.'''
    return requests.get(url).text
