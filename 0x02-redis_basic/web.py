#!/usr/bin/env python3
'''A module requesting caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''The output of fetched data is cached.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''The content of a URL after caching
    and tracking the request are returned.
    '''
    return requests.get(url).text
