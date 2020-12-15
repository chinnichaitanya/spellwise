from operator import itemgetter


def sort_list(data, sort_key, descending=False):
    return sorted(data, key=itemgetter(sort_key), reverse=descending)
