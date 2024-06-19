#!/usr/bin/env python3
"""
Module for caching data in Redis.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for storing data in Redis with a random key.
    """

    def __init__(self):
        """
        Initialize the Cache class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis by key, optionally
        using a callable to convert the data.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable]): A callable to convert
            the data. Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved
            data, optionally converted by fn.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis by key.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[str]: The retrieved string data,
            or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis by key.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[int]: The retrieved integer data,
            or None if the key does not exist.
        """
        return self.get(key, int)
