from typing import List

from ..dictionary import Dictionary
from ..utils import sort_list
from .base import Base


class Levenshtein(Base):
    def __init__(self) -> None:
        super(Levenshtein, self).__init__()

    def _replace(self, a: str, b: str) -> float:
        if a == b:
            return 0
        return 1

    def get_suggestions(self, query_word: str, max_distance: int = 2) -> List[dict]:
        processed_query_word = self._pre_process(query_word)

        def search(dictionary_node: Dictionary, previous_row: list):
            for current_source_letter in dictionary_node.children:
                current_row = [previous_row[0] + 1]

                for i in range(1, len(processed_query_word) + 1):
                    value = min(
                        previous_row[i] + 1,
                        current_row[i - 1] + 1,
                        previous_row[i - 1]
                        + self._replace(
                            current_source_letter, processed_query_word[i - 1]
                        ),
                    )
                    current_row.append(value)

                if (
                    current_row[-1] <= max_distance
                    and dictionary_node.children[current_source_letter].words_at_node
                    is not None
                ):
                    for word in dictionary_node.children[
                        current_source_letter
                    ].words_at_node:
                        suggestions.append({"word": word, "distance": current_row[-1]})

                if min(current_row) <= max_distance:
                    search(dictionary_node.children[current_source_letter], current_row)

        suggestions = list()

        first_row = range(0, len(processed_query_word) + 1)
        search(self._dictionary, first_row)

        suggestions = sort_list(suggestions, "distance")
        return suggestions
