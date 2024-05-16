#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method,
store an instance of the Redis client as a
private variable named _redis
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A method to count how many time the class was accessed.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        A method to wrap the count method.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A method uswd ro record history for a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Used to decorate a function.
        """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


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

    @call_history
    @count_calls
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
