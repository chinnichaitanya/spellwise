# Spellwise

🚀 Extremely fast spelling checker and suggester in Python!

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

The following algorithms are supported currently,

- Edit-distance, [Hall and Dowling (1980)](https://dl.acm.org/doi/10.1145/356827.356830) (based on [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) algorithm)
- Editex, [Zobel and Dart (1996)](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf) (for suggesting phonetically similar words)
- Caverphone 1.0 and Caverphone 2.0 [David Hood (2002)](https://caversham.otago.ac.nz/files/working/ctp060902.pdf) (to identify English names which sound phonetically similar)
- QWERTY Keyboard layout Typographic based correction algorithm (Typox), inspired from [Ahmad, Indrayana, Wibisono, and Ijtihadie (2017)](https://ieeexplore.ieee.org/document/8257147). This implementation might not be the exact one specified in the paper since it is not available to read for free

All the above algorithms use an underlying [Trie](https://en.wikipedia.org/wiki/Trie) based dictionary for efficient storage and fast computation! The implementations of both Edit-distance and Editex algorithms are inspired from the amazing article [Fast and Easy Levenshtein distance using a Trie, by Steve Hanov](http://stevehanov.ca/blog/?id=114).

## 📦 Installation

To be updated soon!

## 🧑‍💻 Usage

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
from spellwise import CaverphoneOne, CaverphoneTwo, Editex, Levenshtein, Typox

# (1) Initialize the desired algorithm
algorithm = Editex() # this can be CaverphoneOne, CaverphoneTwo, Levenshtein or Typox as well

# (2) Index the words / names to the algorithm
# Indexing can be done by adding words from a file
algorithm.add_from_path("<path-to-the-dictionary-file>")
# or by adding them manually
algorithm.add_words(["spell", "spelling", "check"])

# (3) Fetch the suggestions for the word
suggestions = algorithm.get_suggestions("spellin")
# The `suggestions` is a list of dict with fields `word` and `distance`
# [{"word": ..., "distance": ...}, ...]
print(suggestions)

```

## 💡 Analysis of each algorithm

There are many algorithms currently available in the package and each one of them are used for different purposes.
We will discuss each algorithm in specific in the following sections.

### (1) Levenshtein

The `Levenshtein` algorithm is the baseline and most popular method to identify the closest correct words given the mispelled word, based on the edit-distance (number of insertions, deletions and replacements) between the given word and correct word.

```python
from spellwise import Levenshtein

levenshtein = Levenshtein()
levenshtein.add_from_path("examples/data/american-english")

suggestions = levenshtein.get_suggestions("run")
# Print the top 10 suggestions
print("Word \t Distance")
print("=================")
for suggestion in suggestions[0:10]:
    print("{} \t {}".format(suggestion.get("word"), suggestion.get("distance")))

```

Levenshtein provides the following,

```shell
Word 	 Distance
=================
run 	 0
bun 	 1
dun 	 1
fun 	 1
gun 	 1
hun 	 1
jun 	 1
jun 	 1
mun 	 1
nun 	 1

```

### (2) Editex

The `Editex` algorithm provides suggestions of words which are phonetically closed to the given word. It also uses the edit-distance but has different replacement or deletion costs depending on whether the two letters belong to the same phonetic group or not.

```python
from spellwise import Editex

editex = Editex()
editex.add_from_path("examples/data/american-english")

suggestions = editex.get_suggestions("run")
# Print the top 10 suggestions
print("Word \t Distance")
print("=================")
for suggestion in suggestions[0:10]:
    print("{} \t {}".format(suggestion.get("word"), suggestion.get("distance")))

```

Editex suggests the following,

```shell
Word 	 Distance
=================
run 	 0
ran 	 1
ron 	 1
ruin 	 1
rum 	 1
bun 	 2
dun 	 2
dunn 	 2
fun 	 2
gun 	 2

```

Notice that the `Levenshtein` algorithm computes the distance between `run` and `bun` to be 1 since there is only one replacement necessary. On the other hand, `Editex` algorithm computes this distance to be 2 since phonetically, the words are farther apart.

### (3) Caverphone 1.0 and Caverphone 2.0

The Caverphone algorithm was developed as a part of the Caversham project to phonetically identify the names of different instances of the same person from different sources. In other words, it can be used for phonetically identifying duplicate entries of an entity or word. The difference between the v1 and v2 of the algorithm is in the pre-precessing of the words before comparing.

```python
from spellwise import CaverphoneTwo # or CaverphoneOne

caverphone = CaverphoneTwo()
caverphone.add_from_path("examples/data/american-english")

suggestions = caverphone.get_suggestions("run")
# Print the top 10 suggestions
print("Word \t Distance")
print("=================")
for suggestion in suggestions[0:10]:
    print("{} \t {}".format(suggestion.get("word"), suggestion.get("distance")))

```

Caverphone v2 provides the following suggestions,

```shell
Word 	 Distance
=================
rain 	 0
ran 	 0
rein 	 0
rene 	 0
roan 	 0
ron 	 0
ruin 	 0
run 	 0
rune 	 0
wren 	 0

```

### (4) Typox

The `Typox` is a Typographic based correction algorithm optimised for correcting typos in QWERTY keyboard. This is based on the philosophy of the `Editex` algorithm by grouping of letters is based on their locations on the keyboard, instead of matching them phonetically. This might not be the exact implementation of the algorithm since the original paper is not available to read for free.

```python
from spellwise import Typox

typox = Typox()
typox.add_from_path("examples/data/american-english")

suggestions = typox.get_suggestions("ohomr")
# Print the top 10 suggestions
print("Word \t Distance")
print("=================")
for suggestion in suggestions[0:10]:
    print("{} \t {}".format(suggestion.get("word"), suggestion.get("distance")))

```

Typox provides the following words,

```shell
Word 	 Distance
=================
home 	 2
phone 	 2
```

Notice that `Typox` didn not suggest words like `choke`, `come`, `chore`, `chose` etc., (which `Levenshtein` would suggest) even though they are of edit-distance 2 with the word `ohome`. But it rather suggests closest wrods based on the QWERTY keyboard layout which are `phone` and `home`.

## ⚡️ Memory and Time profiling

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

## 🙌 Contributing

Please feel free to raise PRs! 😃

There are so many algorithms to be added and improvements to be made to this package.
This is still in an early version and would love to have you contribute!

## 📝 References

- https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf
- https://scholar.harvard.edu/jfeigenbaum/software/editex
- https://github.com/J535D165/FEBRL-fork-v0.4.2/blob/master/stringcmp.py
- https://caversham.otago.ac.nz/files/working/ctp060902.pdf
- https://en.wikipedia.org/wiki/Caverphone
- https://ieeexplore.ieee.org/document/8257147
- https://www.semanticscholar.org/paper/Edit-distance-weighting-modification-using-phonetic-Ahmad-Indrayana/0d74db8a20f7b46b98c2c77750b9b973a3e4a7b2
- http://stevehanov.ca/blog/?id=114
