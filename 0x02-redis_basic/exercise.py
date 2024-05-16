#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method,
store an instance of the Redis client as a
private variable named _redis
"""
import redis
import uuid
from typing import Union


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
