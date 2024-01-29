#!/usr/bin/env python3

"""
Module for simple helper function for pagination
"""

from typing import Tuple

ret_typ = Tuple[int, int]


def index_range(page: int, page_size: int) -> ret_typ:
    """
    Helper function that retrieves index range from a given page
    and page size
    Args:
        page (int):
        page_size (int):
    Returns:
        Returns tupple of ints
    """
    if isinstance(page, int) and isinstance(page_size, int):
        return ((page - 1) * page_size, page_size * page)
    raise TypeError('Expected `page` and `page_size` to be ints')
