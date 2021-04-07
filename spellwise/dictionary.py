from typing import List, Tuple


class Dictionary(object):
    """Trie based dictionary class for indexing words to consider for spelling correction"""

    def __init__(self) -> None:
        self.words_at_node = None
        self.children = {}

    def add_words(self, words: List[Tuple[str, str]]) -> None:
        """Add words to index to the Trie dictionary

        Args:
            words (List[Tuple[str, str]]): The list of words to index to the dictionary
        """

        for word in words:
            processed_word, actual_word = word
            trie_node = self
            for letter in processed_word:
                if letter not in trie_node.children:
                    trie_node.children.update({letter: Dictionary()})
                trie_node = trie_node.children[letter]

            if trie_node.words_at_node is None:
                trie_node.words_at_node = list()
            trie_node.words_at_node.append(actual_word)

    # def remove_words(self, processed_words):
    #     for word in processed_words:
    #         word_exists = self.has_word(word)

    #         # If the word exists in the Dictionary, iterate again and delete
    #         if word_exists:
    #             trie_node = self
    #             for letter in word.lower():
    #                 if letter in trie_node.children:
    #                     child_trie_node = trie_node.children[letter]
    #                     num_children = len(child_trie_node.children.keys())
    #                     if (
    #                         num_children == 1 and child_trie_node.words_at_node is None
    #                     ) or (num_children == 0):
    #                         _ = trie_node.children.pop(letter)
    #                         break

    #                     # Update trie node to iterate over the children
    #                     trie_node = trie_node.children[letter]

    # def has_word(self, word):
    #     word_length = len(word)
    #     trie_node = self
    #     for i, letter in enumerate(word.lower()):
    #         if letter in trie_node.children:
    #             trie_node = trie_node.children[letter]
    #             if i == word_length - 1:
    #                 if trie_node.words_at_node is not None:
    #                     return True
    #                 else:
    #                     return False
    #         else:
    #             return False

    # def add_from_path(self, path=None):
    #     if path is not None:
    #         path_file = open(path, "r").read().split()
    #         for word in path_file:
    #             self.add_words([word.lower().strip()])


# if __name__ == "__main__":
#     dictionary = Dictionary()
#     dictionary.add_words(["spell", "spelling", "checker"])

#     assert dictionary.has_word("spell") is True
#     dictionary.remove_words(["spell"])
#     assert dictionary.has_word("spell") is False
