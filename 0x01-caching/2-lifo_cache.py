#!/usr/bin/python3
"""Class: LIFO Cache Replacement Implementation
"""
from threading import RLock

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """
    Implementation of LIFO Cache

    Attributes:
    """
    def __init__(self):
        """ Method Instantiation, sets instance attributes
        """
        super().__init__()
        self.__keys = []
        self.__rlock = RLock()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            outKey = self._balance(key)
            with self.__rlock:
                self.cache_data.update({key: item})
            if outKey is not None:
                print('DISCARD: {}'.format(outKey))

    def get(self, key):
        """ Get item by key
        """
        with self.__rlock:
            return self.cache_data.get(key, None)

    def _balance(self, keyIn):
        """ Removes earliest item from cache at MAX size
        """
        outKey = None
        with self.__rlock:
            keysLen = len(self.__keys)
            if keyIn not in self.__keys:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    outKey = self.__keys.pop(keysLen - 1)
                    self.cache_data.pop(outKey)
            else:
                self.__keys.remove(keyIn)
            self.__keys.insert(keysLen, keyIn)
        return outKey
