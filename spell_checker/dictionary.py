class Dictionary(object):
    def __init__(self):
        self.word_at_node = None
        self.children = {}

    def add_words(self, words):
        for word in words:
            trie_node = self
            for letter in word.lower():
                if letter not in trie_node.children:
                    trie_node.children.update({letter: Dictionary()})
                trie_node = trie_node.children[letter]

            trie_node.word_at_node = word

    def remove_words(self, words):
        for word in words:
            word_exists = self.has_word(word)

            # If the word exists in the Dictionary, iterate again and delete
            if word_exists:
                trie_node = self
                for letter in word.lower():
                    if letter in trie_node.children:
                        child_trie_node = trie_node.children[letter]
                        num_children = len(child_trie_node.children.keys())
                        if (
                            num_children == 1 and child_trie_node.word_at_node is None
                        ) or (num_children == 0):
                            _ = trie_node.children.pop(letter)
                            break

                        # Update trie node to iterate over the children
                        trie_node = trie_node.children[letter]

    def has_word(self, word):
        word_length = len(word)
        trie_node = self
        for i, letter in enumerate(word.lower()):
            if letter in trie_node.children:
                trie_node = trie_node.children[letter]
                if i == word_length - 1:
                    if trie_node.word_at_node is not None:
                        return True
                    else:
                        return False
            else:
                return False

    def add_from_path(self, path=None):
        if path is not None:
            path_file = open(path, "r").read().split()
            for word in path_file:
                self.add_words([word.lower().strip()])


if __name__ == "__main__":
    dictionary = Dictionary()
    dictionary.add_words(["spell", "spelling", "checker"])

    assert dictionary.has_word("spell") is True
    dictionary.remove_words(["spell"])
    assert dictionary.has_word("spell") is False
