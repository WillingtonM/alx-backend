#!/usr/bin/env python3
"""
Module for simple helper function for pagination
"""
import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
        Retrieves index range from given page and page size.
    """
    return ((page-1) * page_size, page_size * page)


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
        """
            Retrieves and return the appropriate page of the dataset
        """
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0
        strt, end = index_range(page, page_size)
        data_set = self.dataset()
        if strt > len(data_set):
            return []
        return data_set[strt:end]
