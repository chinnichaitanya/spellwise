from operator import itemgetter
from typing import List


def sort_list(data: List[dict], sort_key: str, descending: bool = False) -> List[dict]:
    """Utility function to sort the list of dictionaries according to the
        `sort_key` field

    Args:
        data (List[dict]): The list of dictionary objects which needs to be
            sorted
        sort_key (str): The key in the dictionary with respect to which
            the sorting should happen
        descending (bool, optional): Indicate whether the sorting should be
            in ascending order or in descending order. Defaults to False

    Returns:
        List[dict]: The sorted list of dictionaries, according to the
            `sort_key` and `descending` variables
    """

    return sorted(data, key=itemgetter(sort_key), reverse=descending)
