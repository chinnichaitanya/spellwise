from typing import List

from ..utils import sort_list
from .base import Base


class Soundex(Base):
    """The Soundex algorithm class for for identifying English words which are phonetically similar

    Reference: https://nlp.stanford.edu/IR-book/html/htmledition/phonetic-correction-1.html
    """

    def __init__(self) -> None:
        """The constructor for the class"""

        super(Soundex, self).__init__()

    def _pre_process(self, word: str) -> str:
        """Pre-processor for Soundex

        Args:
            word (str): The word to be pre-processed

        Returns:
            str: The pre-processed word
        """

        word = word.lower()
        word = "".join(_w for _w in word if _w in self._alphabet)

        first_letter = word[0]
        word = word[1:]

        for _w in "aeiouhwy":
            word = word.replace(_w, "0")

        for _w in "bfpv":
            word = word.replace(_w, "1")
        for _w in "cgjkqsxz":
            word = word.replace(_w, "2")
        for _w in "dt":
            word = word.replace(_w, "3")
        word = word.replace("l", "4")
        for _w in "mn":
            word = word.replace(_w, "5")
        word = word.replace("r", "6")

        for _w in "0123456789":
            while _w * 2 in word:
                word = word.replace(_w * 2, _w)

        word = word.replace("0", "")
        word = first_letter + word + "0" * 3
        word = word[0:4]

        return word

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

    def get_suggestions(self, query_word: str, max_distance: int = 0) -> List[dict]:
        """Get suggestions based on the edit-distance using dynamic-programming approach

        Args:
            query_word (str): The given query word for suggesting indexed words
            max_distance (int, optional): The maximum distance between the words indexed and the query word. Defaults to 0

        Returns:
            List[dict]: The word suggestions with their corresponding distances
        """

        processed_query_word = self._pre_process(query_word)

        def search(dictionary_node, previous_row):
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
