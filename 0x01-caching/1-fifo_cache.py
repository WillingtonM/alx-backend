#!/usr/bin/python3
""" Class: FIFO Cache Replacement Implementation
"""
from threading import RLock

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    Implementation of FIFO Cache

    Attributes:
    """
    def __init__(self):
        """ Method Instantiation, sets instance attributes
        """
        super().__init__()
        self.__keys = []
        self.__rlock = RLock()

    def put(self, key, item):
        """ Add item in cache
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
        """ Removes oldest item from cache at MAX size
        """
        outKey = None
        with self.__rlock:
            if keyIn not in self.__keys:
                keysLen = len(self.__keys)
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    outKey = self.__keys.pop(0)
                    self.cache_data.pop(outKey)
                self.__keys.insert(keysLen, keyIn)
        return outKey
