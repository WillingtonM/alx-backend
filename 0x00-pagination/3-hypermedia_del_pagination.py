#!/usr/bin/env python3
"""
Module for simple helper function for pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    CSV_DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
            Initializes server instance.
        """
        self.__dataset = None
        self.__indexed_dataset = None

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

    def indexed_dataset(self) -> Dict[int, List]:
        """
            Data indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            data_set = self.dataset()
            self.__indexed_dataset = {
                d: data_set[d] for d in range(len(data_set))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
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
        assert 0 <= index < len(self.dataset())

        indxd_dataset = self.indexed_dataset()
        indexed_page = {}

        ind = index
        while (len(indexed_page) < page_size and ind < len(self.dataset())):
            if ind in indxd_dataset:
                indexed_page[ind] = indxd_dataset[ind]
            ind += 1

        pg = list(indexed_page.values())
        page_indices = indexed_page.keys()

        return {
            'index': index,
            'next_index': max(page_indices) + 1,
            'page_size': len(pg),
            'data': pg
        }
