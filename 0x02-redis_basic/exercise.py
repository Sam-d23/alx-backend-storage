#!/usr/bin/env python3
"""
Module for caching data in Redis and counting method calls.
"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count method calls.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store inputs and outputs in Redis.
        """
        input_str = str(args)
        self._redis.rpush(f"{method.__qualname__}:inputs", input_str)
        output_str = str(method(self, *args, **kwargs))
        self._redis.rpush(f"{method.__qualname__}:outputs", output_str)
        return output_str

    return wrapper


def replay(fn: Callable):
    '''The history of calls of a particular function is displayed.'''
    r = redis.Redis()
    func_name = fn.__qualname__
    count = r.get(func_name)
    try:
        count = int(count.decode("utf-8"))
    except Exception:
        count = 0
    print("{} was called {} times:".format(func_name, count))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    """
    Cache class for storing data in Redis with
    counting and history functionalities.
    """

    def __init__(self):
        """
        Initialize the Cache class with a Redis
        instance and flush the database.
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The key under which the data is stored.
        """
        rkey = str(uuid4())
        self._redis.set(rkey, data)
        return rkey

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis by key, optionally
        using a callable to convert the data.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable]): A callable to
            convert the data. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved data,
            optionally converted by fn.
        """
        value = self._redis.get(key)
        if value is not None and fn:
            try:
                value = fn(value)
            except Exception as e:
                print(f"Error converting value for key {key}: {e}")
                value = None
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from Redis by key.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            str: The retrieved string data, or an
            empty string if the key does not exist.
        """
        value = self._redis.get(key)
        if value:
            try:
                return value.decode("utf-8")
            except Exception as e:
                print(f"Error decoding value for key {key}: {e}")
        return ""

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis by key.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            int: The retrieved integer data,
            or 0 if the key does not exist or conversion fails.
        """
        value = self._redis.get(key)
        if value:
            try:
                return int(value.decode("utf-8"))
            except (ValueError, TypeError) as e:
                print(f"Error converting value for key {key}: {e}")
        return 0
