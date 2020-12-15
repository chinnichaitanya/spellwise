from ..dictionary import Dictionary
from ..utils import sort_list


class Levenshtein(object):
    def __init__(self, dictionary):
        if type(dictionary) is not Dictionary:
            raise TypeError(
                "Expected `dictionary` to be of type {}. Received {}".format(
                    Dictionary.__name__, type(dictionary)
                )
            )

        self.dictionary = dictionary

    def _replace(self, a, b):
        if a == b:
            return 0
        return 1

    def get_suggestions(self, query_word, max_distance=2):
        def search(dictionary_node, previous_row):
            for current_source_letter in dictionary_node.children:
                current_row = [previous_row[0] + 1]

                for i in range(1, len(query_word)):
                    value = min(
                        previous_row[i] + 1,
                        current_row[i - 1] + 1,
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
                    search(dictionary_node.children[current_source_letter], current_row)

        suggestions = list()

        for source_letter in self.dictionary.children:
            first_row = [0] * (len(query_word))
            first_row[0] = self._replace(query_word[0], source_letter)
            for i in range(1, len(first_row)):
                first_row[i] = first_row[i - 1] + 1

            search(self.dictionary.children[source_letter], first_row)

        suggestions = sort_list(suggestions, "distance")
        return suggestions
