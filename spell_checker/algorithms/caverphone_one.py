from typing import List

from ..utils import sort_list
from .base import Base


class CaverphoneOne(Base):
    """The Caverphone 1.0 algorithm class for for identifying English names which sound phonetically similar

    Reference: https://caversham.otago.ac.nz/files/working/ctp060902.pdf
    """

    def __init__(self) -> None:
        """The constructor for the class"""

        super(CaverphoneOne, self).__init__()

    def _pre_process(self, word: str) -> str:
        """Pre-processor for Caverphone 1.0

        Args:
            word (str): The word to be pre-processed

        Returns:
            str: The pre-processed word
        """

        word = word.lower()
        word = "".join(_w for _w in word if _w in self._alphabet)

        if word[0:5] == "cough":
            word = "cou2f" + word[5:]
        if word[0:5] == "rough":
            word = "rou2f" + word[5:]
        if word[0:5] == "tough":
            word = "tou2f" + word[5:]
        if word[0:6] == "enough":
            word = "enou2f" + word[5:]
        if word[0:2] == "gn":
            word = "2n" + word[2:]
        if word[-2:] == "mb":
            word = word[0:-2] + "m2"

        word = word.replace("cq", "2q")
        word = word.replace("ci", "si")
        word = word.replace("ce", "se")
        word = word.replace("cy", "sy")
        word = word.replace("tch", "2ch")
        word = word.replace("c", "k")
        word = word.replace("q", "k")
        word = word.replace("x", "k")
        word = word.replace("v", "f")
        word = word.replace("dg", "2g")
        word = word.replace("tio", "sio")
        word = word.replace("tia", "sia")
        word = word.replace("d", "t")
        word = word.replace("ph", "fh")
        word = word.replace("b", "p")
        word = word.replace("sh", "s2")
        word = word.replace("z", "s")

        if word[0:1] in self._vowels:
            word = "A" + word[1:]
        for _v in self._vowels:
            word = word.replace(_v, "3")

        word = word.replace("3gh3", "3kh3")
        word = word.replace("gh", "22")
        word = word.replace("g", "k")

        for _w in "stpkfmn":
            while _w * 2 in word:
                word = word.replace(_w * 2, _w)
            word = word.replace(_w, _w.upper())

        word = word.replace("w3", "W3")
        word = word.replace("wy", "Wy")
        word = word.replace("wh3", "Wh3")
        word = word.replace("why", "Why")
        word = word.replace("w", "2")

        if word[0:1] == "h":
            word = "A" + word[1:]
        word = word.replace("h", "2")

        word = word.replace("r3", "R3")
        word = word.replace("ry", "Ry")
        word = word.replace("r", "2")
        word = word.replace("l3", "L3")
        word = word.replace("ly", "Ly")
        word = word.replace("l", "2")
        word = word.replace("j", "y")
        word = word.replace("y3", "Y3")
        word = word.replace("y", "2")
        word = word.replace("2", "")
        word = word.replace("3", "")
        word = word + "1" * 6
        word = word[0:6]

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
