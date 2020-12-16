# Python Spelling Checker

Extremely fast spelling checker and suggester in Python! Currently supports the following algorithms,

- Edit-distance, [Hall and Dowling (1980)](https://dl.acm.org/doi/10.1145/356827.356830) (based on [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) algorithm)
- Editex, [Zobel and Dart (1996)](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf) (for suggesting phonetically similar words)

Both the above algorithm use an underlying [Trie](https://www.wikiwand.com/en/Trie) based dictionary for efficient storage and fast computation! The implementations of both Edit-distance and Editex algorithms are inspired from the amazing article [Fast and Easy Levenshtein distance using a Trie, by Steve Hanov](http://stevehanov.ca/blog/?id=114).

## References

- https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf
- https://scholar.harvard.edu/jfeigenbaum/software/editex
- https://github.com/J535D165/FEBRL-fork-v0.4.2/blob/master/stringcmp.py
- http://stevehanov.ca/blog/?id=114
