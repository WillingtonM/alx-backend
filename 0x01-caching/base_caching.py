#!/usr/bin/python3
""" BaseCaching Class
"""


class BaseCaching():
    """ BaseCaching defines:
        constants of caching system where data are stored
    """
    MAX_ITEMS = 4

    def __init__(self):
        """ Initiliaze class
        """
        self.cache_data = {}

    def print_cache(self):
        """ Print cache
        """
        print("Current cache:")
        for k in sorted(self.cache_data.keys()):
            print("{}: {}".format(k, self.cache_data.get(k)))

    def put(self, key, item):
        """ Add item in cache
        """
        raise NotImplementedError("put must be implemented in your cache class")

    def get(self, key):
        """ Get item by key
        """
        raise NotImplementedError("get must be implemented in your cache class")
