from typing import List

from ..utils import sort_list
from .base import Base


class Editex(Base):
    """The Editex algorithm class for suggesting phonetically similar words

    Reference: https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf
    """

    def __init__(self, group_cost: float = 1, non_group_cost: float = 2) -> None:
        """The constructor for the class

        Args:
            group_cost (float, optional): The cost to replace of delete when the letters belong to the group. Defaults to 1
            non_group_cost (float, optional): The cost to replace of delete when the letters do not belong to the group. Defaults to 2
        """

        super(Editex, self).__init__()

        self.GROUP_COST = group_cost
        self.NON_GROUP_COST = non_group_cost

    def _letters_in_group(self, a: str, b: str) -> bool:
        """Determine if the letters are in the same group or not

        Args:
            a (str): First letter
            b (str): Second letter

        Returns:
            bool: Whether the letters belong to the same group or not
        """

        value_a = 0
        value_b = 0
        for power, group in enumerate(
            [
                ("a", "e", "i", "o", "u", "y"),
                ("b", "p"),
                ("c", "k", "q"),
                ("d", "t"),
                ("l", "r"),
                ("m", "n"),
                ("g", "j"),
                ("f", "p", "v"),
                ("x", "s", "z"),
                ("c", "s", "z"),
            ]
        ):
            if a in group:
                value_a += pow(2, power)
            if b in group:
                value_b += pow(2, power)

        if (value_a & value_b) > 0:
            return True
        else:
            return False

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
        elif self._letters_in_group(a, b):
            return self.GROUP_COST
        return self.NON_GROUP_COST

    def _delete(self, a: str, b: str) -> float:
        """The cost to delete the letter in query word with the target word

        Args:
            a (str): First letter
            b (str): Second letter

        Returns:
            float: The cost to delete the letters
        """

        if a == b:
            return 0
        elif self._letters_in_group(a, b) or (a in ["h", "w"] and a != b):
            return self.GROUP_COST
        return self.NON_GROUP_COST

    def get_suggestions(self, query_word: str, max_distance: int = 2) -> List[dict]:
        """Get suggestions based on the edit-distance using dynamic-programming approach

        Args:
            query_word (str): The given query word for suggesting indexed words
            max_distance (int, optional): The maximum distance between the words indexed and the query word. Defaults to 2

        Returns:
            List[dict]: The word suggestions with their corresponding distances
        """

        processed_query_word = self._pre_process(query_word)

        def search(dictionary_node, parent_source_letter, previous_row):
            """Search for the candidates in the given dictionary node's children

            Args:
                dictionary_node (Dictionary): The node in the Trie dictionary
                previous_row (list): The previous row in the dynamic-programming approach
            """

            for current_source_letter in dictionary_node.children:
                current_row = [
                    previous_row[0]
                    + self._delete(parent_source_letter, current_source_letter)
                ]

                for i in range(1, len(processed_query_word) + 1):
                    increment_source = self._delete(
                        parent_source_letter, current_source_letter
                    )
                    if i == 1:
                        increment_target = self.NON_GROUP_COST
                    else:
                        increment_target = self._delete(
                            processed_query_word[i - 2], processed_query_word[i - 1]
                        )

                    value = min(
                        previous_row[i] + increment_source,
                        current_row[i - 1] + increment_target,
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
                    search(
                        dictionary_node.children[current_source_letter],
                        current_source_letter,
                        current_row,
                    )

        suggestions = list()

        first_row = [0] * (len(processed_query_word) + 1)
        first_row[1] = self.NON_GROUP_COST
        for i in range(2, len(processed_query_word) + 1):
            first_row[i] = first_row[i - 1] + self._delete(
                processed_query_word[i - 2], processed_query_word[i - 1]
            )
        for source_letter in self._dictionary.children:
            second_row = [self.NON_GROUP_COST]
            for i in range(1, len(processed_query_word) + 1):
                increment_source = self.NON_GROUP_COST
                if i == 1:
                    increment_target = self.NON_GROUP_COST
                else:
                    increment_target = self._delete(
                        processed_query_word[i - 2], processed_query_word[i - 1]
                    )
                value = min(
                    first_row[i] + increment_source,
                    second_row[i - 1] + increment_target,
                    first_row[i - 1]
                    + self._replace(processed_query_word[i - 1], source_letter),
                )
                second_row.append(value)

            search(self._dictionary.children[source_letter], source_letter, second_row)

        suggestions = sort_list(suggestions, "distance")
        return suggestions
