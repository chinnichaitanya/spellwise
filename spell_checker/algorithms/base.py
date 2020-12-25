from ..dictionary import Dictionary


class Base(object):
    def __init__(self):
        self._dictionary = Dictionary()

    def _pre_process(self, word):
        return word

    def add_words(self, words):
        processed_actual_words = [(self._pre_process(word), word) for word in words]
        self._dictionary.add_words(processed_actual_words)

    def add_from_path(self, path=None):
        if path is not None:
            path_file = open(path, "r").read().split()
            for word in path_file:
                self.add_words([word.lower().strip()])
