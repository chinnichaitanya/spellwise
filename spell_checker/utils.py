from operator import itemgetter
from typing import List


def sort_list(data: List[dict], sort_key: str, descending: bool = False) -> List[dict]:
    return sorted(data, key=itemgetter(sort_key), reverse=descending)
