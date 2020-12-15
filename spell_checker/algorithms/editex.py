from ..dictionary import Dictionary
from ..utils import sort_list


class Editex(object):
    def __init__(self, dictionary):
        if type(dictionary) is not Dictionary:
            raise TypeError(
                "Expected `dictionary` to be of type {}. Received {}".format(
                    Dictionary.__name__, type(dictionary)
                )
            )

        self.dictionary = dictionary

    def _letters_code(self, a, b):
        values = [0, 0]
        letters = [a, b]
        for i in [0, 1]:
            if letters[i] in ["a", "e", "i", "o", "u", "y"]:
                values[i] += pow(2, 9)
            if letters[i] in ["b", "p"]:
                values[i] += pow(2, 8)
            if letters[i] in ["c", "k", "q"]:
                values[i] += pow(2, 7)
            if letters[i] in ["d", "t"]:
                values[i] += pow(2, 6)
            if letters[i] in ["l", "r"]:
                values[i] += pow(2, 5)
            if letters[i] in ["m", "n"]:
                values[i] += pow(2, 4)
            if letters[i] in ["g", "j"]:
                values[i] += pow(2, 3)
            if letters[i] in ["f", "p", "v"]:
                values[i] += pow(2, 2)
            if letters[i] in ["x", "s", "z"]:
                values[i] += pow(2, 1)
            if letters[i] in ["c", "s", "z"]:
                values[i] += pow(2, 0)
        if (values[0] & values[1]) > 0:
            return True
        else:
            return False

    def _replace(self, a, b):
        if a == b:
            return 0
        elif self._letters_code(a, b):
            return 1
        return 2

    def _delete(self, a, b):
        if a == b:
            return 0
        elif self._letters_code(a, b) or ((a == "h" or a == "w") and a != b):
            return 1
        return 2

    def get_suggestions(self, query_word, max_distance=2):
        def search(dictionary_node, parent_source_letter, previous_row):
            for current_source_letter in dictionary_node.children:
                current_row = [
                    previous_row[0]
                    + self._delete(parent_source_letter, current_source_letter)
                ]

                for i in range(1, len(query_word)):
                    value = min(
                        previous_row[i]
                        + self._delete(parent_source_letter, current_source_letter),
                        current_row[i - 1]
                        + self._delete(query_word[i - 1], query_word[i]),
                        previous_row[i - 1]
                        + self._replace(current_source_letter, query_word[i]),
                    )
                    current_row.append(value)

                if (
                    current_row[-1] <= max_distance
                    and dictionary_node.children[current_source_letter].word_at_node
                    is not None
                ):
                    suggestions.append(
                        {
                            "word": dictionary_node.children[
                                current_source_letter
                            ].word_at_node,
                            "distance": current_row[-1],
                        }
                    )

                if min(current_row) <= max_distance:
                    search(
                        dictionary_node.children[current_source_letter],
                        current_source_letter,
                        current_row,
                    )

        suggestions = list()

        for source_letter in self.dictionary.children:
            first_row = [0] * (len(query_word))
            first_row[0] = self._replace(query_word[0], source_letter)
            for i in range(1, len(first_row)):
                first_row[i] = first_row[i - 1] + self._delete(
                    query_word[i - 1], query_word[i]
                )

            search(self.dictionary.children[source_letter], source_letter, first_row)

        suggestions = sort_list(suggestions, "distance")
        return suggestions
