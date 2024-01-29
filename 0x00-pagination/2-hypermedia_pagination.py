#!/usr/bin/env python3
"""
Module for simple helper function for pagination
"""

import csv
from math import ceil
from typing import List

index_range = __import__('0-simple_helper_function').index_range


class Server:
    """
        This is a server class to paginate database of popular baby names.
    """
    CSV_DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
            Initializes server instance.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
            Cached
        """
        if self.__dataset is None:
            with open(self.CSV_DATA_FILE) as csv_file:
                csv_reader = csv.reader(csv_file)
                data_set = [r for r in csv_reader]
            self.__dataset = data_set[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Return page of dataset. """
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        strt, end = index_range(page, page_size)

        try:
            return self.dataset()[strt:end]
        except IndexError:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """ 
            Retrieve or return dict of pagination data.
            Key/value pairs consist of the following:
                page_size - dataset page length 
                page - current page number
                data - dataset page
                next_page - next page if there is one
                prev_page - previous page if there is one
                total_pages - total pages
        """
        data_total = len(self.dataset())
        pages_total = ceil(data_total / page_size)
        pg_data = self.get_page(page, page_size)

        return {
            'page_size': len(pg_data),
            'page': page,
            'data': pg_data,
            'next_page': page + 1 if page < pages_total else None,
            'prev_page': page - 1 if page != 1 else None,
            'total_pages': pages_total
        }
