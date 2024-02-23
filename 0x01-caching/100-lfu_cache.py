#!/usr/bin/python3
"""Class: LFU Cache Replacement Implementation
"""
from threading import RLock

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    Implementaion of LFUCache(Least frequently used)

    Attributes:
    """
    def __init__(self):
        """ Instantiation method, sets instance attributes
        """
        super().__init__()
        self.__stats = {}
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
            val = self.cache_data.get(key, None)
            if key in self.__stats:
                self.__stats[key] += 1
        return val

    def _balance(self, keyIn):
        """ Removes earliest item from cache at MAX size
        """
        outKey = None
        with self.__rlock:
            if keyIn not in self.__stats:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    outKey = min(self.__stats, key=self.__stats.get)
                    self.cache_data.pop(outKey)
                    self.__stats.pop(outKey)
            self.__stats[keyIn] = self.__stats.get(keyIn, 0) + 1
        return outKey
