#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method,
store an instance of the Redis client as a
private variable named _redis
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    A class to store data in a redis db.
    """
    def __init__(self):
        """
        A method to initialize instances.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        A method used to store new data in the redis db.
        """
        rid = str(uuid.uuid4())
        self._redis.set(rid, data)
        return (rid)

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        A method used to get values from the db.
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        A method to convert get to str.
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        A method to convert get to int
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception as e:
            value = 0
        return value
