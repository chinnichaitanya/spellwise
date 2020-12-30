from typing import List

from ..dictionary import Dictionary


class Base(object):
    """The base class for all the spelling correction and word suggestion algorithms"""

    def __init__(self) -> None:
        self._alphabet = "abcdefghijklmnopqrstuvwxyz"
        self._vowels = "aeiou"
        self._dictionary = Dictionary()

    def _pre_process(self, word: str) -> str:
        """Pre-processor for every word to be indexed and queried.
            Different algorithms might have different pre-processing steps

        Args:
            word (str): The word to be pre-processed

        Returns:
            str: The pre-processed word
        """

        return word.lower()

    def add_words(self, words: List[str]) -> None:
        """Helper method to add words (index) to the dictionary used by the algorithm

        Args:
            words (List[str]): The list of words to be indexed
        """

        processed_actual_words = [(self._pre_process(word), word) for word in words]
        self._dictionary.add_words(processed_actual_words)

    def add_from_path(self, path: str) -> None:
        """Helper method to add words (index) from a file where each line consists of a word.
            This internally calls the `add_words(...)` method for every word

        Args:
            path (str): The path to the file
        """

        if path is not None:
            path_file = open(path, "r").read().split()
            for word in path_file:
                self.add_words([word.lower().strip()])
