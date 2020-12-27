from typing import List

from ..utils import sort_list
from .base import Base


class Editex(Base):
    def __init__(self, group_cost: float = 1, non_group_cost: float = 2) -> None:
        super(Editex, self).__init__()

        self.GROUP_COST = group_cost
        self.NON_GROUP_COST = non_group_cost

    def _letters_in_group(self, a: str, b: str) -> bool:
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
        if a == b:
            return 0
        elif self._letters_in_group(a, b):
            return self.GROUP_COST
        return self.NON_GROUP_COST

    def _delete(self, a: str, b: str) -> float:
        if a == b:
            return 0
        elif self._letters_in_group(a, b) or (a in ["h", "w"] and a != b):
            return self.GROUP_COST
        return self.NON_GROUP_COST

    def get_suggestions(self, query_word: str, max_distance: int = 2) -> List[dict]:
        def search(dictionary_node, parent_source_letter, previous_row):
            for current_source_letter in dictionary_node.children:
                current_row = [
                    previous_row[0]
                    + self._delete(parent_source_letter, current_source_letter)
                ]

                for i in range(1, len(query_word) + 1):
                    increment_source = self._delete(
                        parent_source_letter, current_source_letter
                    )
                    if i == 1:
                        increment_target = self.NON_GROUP_COST
                    else:
                        increment_target = self._delete(
                            query_word[i - 2], query_word[i - 1]
                        )

                    value = min(
                        previous_row[i] + increment_source,
                        current_row[i - 1] + increment_target,
                        previous_row[i - 1]
                        + self._replace(current_source_letter, query_word[i - 1]),
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

        first_row = [0] * (len(query_word) + 1)
        first_row[1] = self.NON_GROUP_COST
        for i in range(2, len(query_word) + 1):
            first_row[i] = first_row[i - 1] + self._delete(
                query_word[i - 2], query_word[i - 1]
            )
        for source_letter in self._dictionary.children:
            second_row = [self.NON_GROUP_COST]
            for i in range(1, len(query_word) + 1):
                increment_source = self.NON_GROUP_COST
                if i == 1:
                    increment_target = self.NON_GROUP_COST
                else:
                    increment_target = self._delete(
                        query_word[i - 2], query_word[i - 1]
                    )
                value = min(
                    first_row[i] + increment_source,
                    second_row[i - 1] + increment_target,
                    first_row[i - 1] + self._replace(query_word[i - 1], source_letter),
                )
                second_row.append(value)

            search(self._dictionary.children[source_letter], source_letter, second_row)

        suggestions = sort_list(suggestions, "distance")
        return suggestions
