# Python Spelling Checker

🚀 Extremely fast spelling checker and suggester in Python! Currently supports the following algorithms,

- Edit-distance, [Hall and Dowling (1980)](https://dl.acm.org/doi/10.1145/356827.356830) (based on [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) algorithm)
- Editex, [Zobel and Dart (1996)](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf) (for suggesting phonetically similar words)
- Caverphone 1.0 and Caverphone 2.0 [David Hood (2002)](https://caversham.otago.ac.nz/files/working/ctp060902.pdf) (to identify English names which sound phonetically similar)
- QWERTY Keyboard layout Typographic based correction algorithm (Typox), inspired from [Ahmad, Indrayana, Wibisono, and Ijtihadie (2017)](https://ieeexplore.ieee.org/document/8257147). This implementation might not be the exact one specified in the paper since it is not available to read for free

All the above algorithms use an underlying [Trie](https://en.wikipedia.org/wiki/Trie) based dictionary for efficient storage and fast computation! The implementations of both Edit-distance and Editex algorithms are inspired from the amazing article [Fast and Easy Levenshtein distance using a Trie, by Steve Hanov](http://stevehanov.ca/blog/?id=114).

## Installation

To be updated soon!

## Usage

Currently there are five algorithms available for use with the following classnames,

- `Levenshtein`
- `Editex`
- `CaverphoneOne`
- `CaverphoneTwo`
- `Typox`

Please check the [`examples/`](https://github.com/chinnichaitanya/python-spell-checker/tree/master/examples) folder for specific usage of each algorithm. But in a general sense, each algorithm has three parts,

- Initialization (initialize the class object for the algorithm to use)
- Index correct words / names (add correct words or names to the dictionary)
- Fetch suggestions (inference)

```python
from spell_checker import import CaverphoneOne, CaverphoneTwo, Editex, Levenshtein, Typox

# (1) Initialize the desired algorithm
algorithm = Editex() # this can be CaverphoneOne, CaverphoneTwo, Levenshtein or Typox as well

# (2) Index the words / names to the algorithm
# Indexing can be done by adding words from a file
algorithm.add_from_path("<path-to-the-dictionary-file>")
# or by adding it manually
algorithm.add_words(["spell", "spelling", "check"])

# (3) Fetch the suggestions for the word
suggestions = algorithm.get_suggestions("spellin")
print(suggestions)

```

## Memory and Time profiling

The following are the usage statistics on MacBook Pro, 2.4 GHz Quad-Core Intel Core i5 with 16 GB RAM.

<table>
    <tr>
        <th>Algorithm</th>
        <th>No. of words</th>
        <th>Memory used</th>
        <th>Time to index</th>
        <th>Time to inference</th>
        <th>Remarks</th>
    </tr>
    <tr>
        <td>Levenshtein</td>
        <td>119,095</td>
        <td>~ 127 MB</td>
        <td>~ 1160 milliseconds</td>
        <td>~ 36 milliseconds</td>
        <td>
            <ul>
                <li>For word "hallo"</li>
                <li>With max distance 2</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Editex</td>
        <td>119,095</td>
        <td>~ 127 MB</td>
        <td>~ 1200 milliseconds</td>
        <td>~ 90 milliseconds</td>
        <td>
            <ul>
                <li>For word "hallo"</li>
                <li>With max distance 2</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Caverphone 1.0</td>
        <td>119,095</td>
        <td>~ 36.7 MB</td>
        <td>~ 1700 milliseconds</td>
        <td>~ 0.2 milliseconds (yes right!)</td>
        <td>
            <ul>
                <li>For word "hallo"</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Caverphone 2.0</td>
        <td>119,095</td>
        <td>~ 99 MB</td>
        <td>~ 2400 milliseconds</td>
        <td>~ 0.4 milliseconds (yes right!)</td>
        <td>
            <ul>
                <li>For word "hallo"</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Typox</td>
        <td>119,095</td>
        <td>~ 127 MB</td>
        <td>~ 1360 milliseconds</td>
        <td>~ 200 milliseconds</td>
        <td>
            <ul>
                <li>For word "hallo"</li>
                <li>With max distance 2</li>
            </ul>
        </td>
    </tr>
</table>

## References

- https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf
- https://scholar.harvard.edu/jfeigenbaum/software/editex
- https://github.com/J535D165/FEBRL-fork-v0.4.2/blob/master/stringcmp.py
- https://caversham.otago.ac.nz/files/working/ctp060902.pdf
- https://en.wikipedia.org/wiki/Caverphone
- https://ieeexplore.ieee.org/document/8257147
- https://www.semanticscholar.org/paper/Edit-distance-weighting-modification-using-phonetic-Ahmad-Indrayana/0d74db8a20f7b46b98c2c77750b9b973a3e4a7b2
- http://stevehanov.ca/blog/?id=114
