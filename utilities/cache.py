from threading import RLock
from cachetools import TTLCache


class Cache:
    def __init__(self, ttl=600, max_size=1024):
        self._cache = TTLCache(maxsize=max_size, ttl=ttl)
        self._lock = RLock()

    def get(self, key):
        with self._lock:
            return self._cache.get(key, None)

    def set(self, key, value):
        with self._lock:
            self._cache[key] = value

    def clear(self):
        with self._lock:
            self._cache.clear()


# Singleton cache instance
cache = Cache()
