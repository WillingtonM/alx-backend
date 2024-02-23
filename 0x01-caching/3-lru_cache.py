#!/usr/bin/python3
"""Class: LRU Cache Replacement Implementation
"""
from threading import RLock

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    Implementation of Cache

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
            keyOut = self._balance(key)
            with self.__rlock:
                self.cache_data.update({key: item})
            if keyOut is not None:
                print('DISCARD: {}'.format(keyOut))

    def get(self, key):
        """ Get item by key
        """
        with self.__rlock:
            val = self.cache_data.get(key, None)
            if key in self.__keys:
                self._balance(key)
        return val

    def _balance(self, keyIn):
        """ Removes earliest item from cache at MAX size
        """
        keyOut = None
        with self.__rlock:
            keysLength = len(self.__keys)
            if keyIn not in self.__keys:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    keyOut = self.__keys.pop(0)
                    self.cache_data.pop(keyOut)
            else:
                self.__keys.remove(keyIn)
            self.__keys.insert(keysLength, keyIn)
        return keyOut
