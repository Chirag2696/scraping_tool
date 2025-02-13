# scraper/cache.py
class Cache:
    def __init__(self):
        self._cache = {}

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, value):
        self._cache[key] = value

    def exists(self, key: str) -> bool:
        return key in self._cache
