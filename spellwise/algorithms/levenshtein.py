from typing import List

from ..dictionary import Dictionary
from ..utils import sort_list
from .base import Base


class Levenshtein(Base):
    """The Levenshtein algorithm class for suggesting words based on edit-distance

    Reference: https://dl.acm.org/doi/10.1145/356827.356830
    """

    def __init__(self) -> None:
        """The constructor for the class"""

        super(Levenshtein, self).__init__()

    def _replace(self, a: str, b: str) -> float:
        """Cost to replace the letter in query word with the target word

        Args:
            a (str): First letter
            b (str): Second letter

        Returns:
            float: The cost to replace the letters
        """

        if a == b:
            return 0
        return 1

    def get_suggestions(self, query_word: str, max_distance: int = 2) -> List[dict]:
        """Get suggestions based on the edit-distance using dynamic-programming approach

        Args:
            query_word (str): The given query word for suggesting indexed words
            max_distance (int, optional): The maximum distance between the words indexed and the query word. Defaults to 2

        Returns:
            List[dict]: The word suggestions with their corresponding distances
        """

        processed_query_word = self._pre_process(query_word)

        def search(dictionary_node: Dictionary, previous_row: list):
            """Search for the candidates in the given dictionary node's children

            Args:
                dictionary_node (Dictionary): The node in the Trie dictionary
                previous_row (list): The previous row in the dynamic-programming approach
            """

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
