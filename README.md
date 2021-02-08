# Spellwise

🚀 Extremely fast spelling checker and suggester in Python!

<a href="https://pypi.org/project/spellwise/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/spellwise"></a>
[![PyPI version](https://badge.fury.io/py/spellwise.svg)](https://badge.fury.io/py/spellwise)
<a href="https://pepy.tech/project/spellwise"><img alt="Downloads" src="https://static.pepy.tech/badge/spellwise"></a>
<a href="https://pypi.org/project/spellwise/#files"><img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/spellwise"></a>
[![License: MIT](https://img.shields.io/pypi/l/spellwise)](https://github.com/chinnichaitanya/spellwise/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

The following algorithms are supported currently,

- Edit-distance, [Hall and Dowling (1980)](https://dl.acm.org/doi/10.1145/356827.356830) (based on [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) algorithm)
- Editex, [Zobel and Dart (1996)](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf) (for suggesting phonetically similar words)
- Soundex (https://nlp.stanford.edu/IR-book/html/htmledition/phonetic-correction-1.html) (for identifying phonetically similar words)
- Caverphone 1.0 and Caverphone 2.0, [David Hood (2002)](https://caversham.otago.ac.nz/files/working/ctp060902.pdf) (to identify English names which sound phonetically similar)
- QWERTY Keyboard layout Typographic based correction algorithm (Typox), inspired by [Ahmad, Indrayana, Wibisono, and Ijtihadie (2017)](https://ieeexplore.ieee.org/document/8257147). This implementation might not be the exact one specified in the paper since it is not available to read for free

All the above algorithms use an underlying [Trie](https://en.wikipedia.org/wiki/Trie) based dictionary for efficient storage and fast computation! Implementations of all the algorithms are inspired by the amazing article [Fast and Easy Levenshtein distance using a Trie, by Steve Hanov](http://stevehanov.ca/blog/?id=114).

## 📦 Installation

The easiest way to install `spellwise` is through `pip`.

```shell
pip install spellwise

```

## 🧑‍💻 Usage

Currently, there are five algorithms available for use with the following classnames,

- `Levenshtein`
- `Editex`
- `Soundex`
- `CaverphoneOne`
- `CaverphoneTwo`
- `Typox`

Please check the [`examples/`](https://github.com/chinnichaitanya/python-spell-checker/tree/master/examples) folder for specific usage of each algorithm. But in a general sense, each algorithm has three parts,

- Initialization (initialize the class object for the algorithm to use)
- Index correct words/names (add correct words or names to the dictionary)
- Fetch suggestions (inference)

```python
from spellwise import (CaverphoneOne, CaverphoneTwo, Editex, Levenshtein,
                       Soundex, Typox)

# (1) Initialize the desired algorithm
algorithm = Editex() # this can be CaverphoneOne, CaverphoneTwo, Levenshtein or Typox as well

# (2) Index the words/names to the algorithm
# Indexing can be done by adding words from a file
algorithm.add_from_path("<path-to-the-dictionary-file>")
# or by adding them manually
algorithm.add_words(["spell", "spelling", "check"])

# (3) Fetch the suggestions for the word
suggestions = algorithm.get_suggestions("spellin")
# The `suggestions` is a list of dict with fields `word` and `distance`
# [{"word": ..., "distance": ...}, ...]
print(suggestions)

# Output would be similar to the following,
# [{'word': 'spelling', 'distance': 2}]

```

The default maximum distance considered varies for different algorithms. It can be changed while fetching the suggestions,

```python
# Fetch suggestions with maximum distance 4
suggestions = algorithm.get_suggestions("spellin", max_distance=4)
# Print the suggestions
print(suggestions)

# Output would be similar to the following,
# [{'word': 'spelling', 'distance': 2}, {'word': 'spell', 'distance': 4}]

```

## 💡 Analysis of each algorithm

There are many algorithms currently available in the package, each suitable for different purposes.
We will discuss each algorithm in specific in the following sections.

### (1) Levenshtein

The `Levenshtein` algorithm is the baseline and most popular method to identify the closest correct words given the misspelt word, based on the edit-distance (number of insertions, deletions and replacements) between the given word and the correctly spelt word.

```python
from spellwise import Levenshtein

# Initialise the algorithm
levenshtein = Levenshtein()
# Index the words from a dictionary
levenshtein.add_from_path("examples/data/american-english")

# Fetch suggestions
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

The `Editex` algorithm provides suggestions of words which are phonetically closed to the given word. It also uses the edit-distance but has a different replacement or deletion costs depending on whether the two letters belong to the same phonetic group or not.

```python
from spellwise import Editex

# Initialise the algorithm
editex = Editex()
# Index the words from a dictionary
editex.add_from_path("examples/data/american-english")

# Fetch suggestions
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

Notice that the `Levenshtein` algorithm computes the distance between `run` and `bun` as 1 (since there is only one replacement necessary). On the other hand, `Editex` algorithm computes this distance as 2 since phonetically, the words are farther apart.

As mentioned above, the Editex algorithm uses different costs for replacement and deletion. These values can be modified for fetching different results.

```python
from spellwise import Editex

# Initialise the algorithm
editex = Editex(group_cost=0.5, non_group_cost=3) # configure the group cost and non-group cost
# Index the words from a dictionary
editex.add_from_path("examples/data/american-english")

# Fetch suggestions
suggestions = editex.get_suggestions("run")
# Print the top 10 suggestions
print("Word \t Distance")
print("=================")
for suggestion in suggestions[0:10]:
    print("{} \t {}".format(suggestion.get("word"), suggestion.get("distance")))

```

Configuring `group_cost=0.5` and `non_group_cost=3` in the above example results in the following suggestions,

```shell
Word 	 Distance
=================
run 	 0
ran 	 0.5
ron 	 0.5
ruin 	 0.5
rum 	 0.5
lan 	 1.0
len 	 1.0
lin 	 1.0
lon 	 1.0
loon 	 1.0

```

### (3) Soundex

The Soundex algorithm, similar to Editex aims to provide phonetically similar words for the give word. It is one of the initial phonetic matching algorithms and many variations exists.

```python
from spellwise import Soundex

# Initialise the algorithm
soundex = Soundex()
# Index the words from a dictionary
soundex.add_from_path("examples/data/american-english")

# Fetch suggestions
suggestions = soundex.get_suggestions("run")
# Print the top 10 suggestions
print("Word \t Distance")
print("=================")
for suggestion in suggestions[0:10]:
    print("{} \t {}".format(suggestion.get("word"), suggestion.get("distance")))

```

Soundex suggests the following,

```shell
Word 	 Distance
=================
rain 	 0
rainy 	 0
ram 	 0
ram 	 0
rama 	 0
ramie 	 0
ran 	 0
ranee 	 0
rayon 	 0
ream 	 0

```

### (4) Caverphone 1.0 and Caverphone 2.0

The Caverphone algorithm was developed as a part of the Caversham project to phonetically identify the names of different instances of the same person from various sources. In other words, it is used for phonetically identifying duplicate entries of an entity or a word. The difference between the v1 and v2 of the algorithm is in the pre-processing of words during indexing.

```python
from spellwise import CaverphoneTwo # or CaverphoneOne

# Initialise the algorithm
caverphone = CaverphoneTwo()
# Index the words from a dictionary
caverphone.add_from_path("examples/data/american-english")

# Fetch suggestions
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

### (5) Typox

The `Typox` is a Typographic based correction algorithm optimised for correcting typos in QWERTY keyboard. This is similar to the `Editex` algorithm, except that the letters are grouped based on their locations on the keyboard, instead of grouping them phonetically. The original paper is not available to read for free, and hence this might not be its exact implementation.

```python
from spellwise import Typox

# Initialise the algorithm
typox = Typox()
# Index the words from a dictionary
typox.add_from_path("examples/data/american-english")

# Fetch suggestions
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

Notice that `Typox` did not suggest words like `choke`, `come`, `chore`, `chose` etc., (which `Levenshtein` would suggest) even though they are of edit-distance 2 with the word `ohome`. But it rather suggests closest words based on the QWERTY keyboard layout which are `phone` and `home`.

As mentioned above, the Typox algorithm is similar to Editex and uses different costs for replacement and deletion. These values can be modified for fetching different results.

```python
from spellwise import Typox

# Initialise the algorithm
typox = Typox(group_cost=0.5, non_group_cost=3) # configure the group cost and non-group cost
# Index the words from a dictionary
typox.add_from_path("examples/data/american-english")

# Fetch suggestions
suggestions = typox.get_suggestions("ohomr")
# Print the top 10 suggestions
print("Word \t Distance")
print("=================")
for suggestion in suggestions[0:10]:
    print("{} \t {}".format(suggestion.get("word"), suggestion.get("distance")))

```

Typox provides the following suggestion for the word `ohomr` after setting the `group_cost=0.5` and `non_group_cost=3`.

```shell
Word 	 Distance
=================
phone 	 1.5
phoned 	 2.0
phones 	 2.0

```

## ⚡️ Memory and Time profiling

The following are the usage statistics on a MacBook Pro, 2.4 GHz Quad-Core Intel Core i5 with 16 GB RAM.

<table>
    <tr>
        <th>Algorithm</th>
        <th>No. of words</th>
        <th>Corpus size on disk</th>
        <th>Memory used</th>
        <th>Time to index</th>
        <th>Time to inference</th>
        <th>Remarks</th>
    </tr>
    <tr>
        <td>Levenshtein</td>
        <td>119,095</td>
        <td>1.1 MB</td>
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
        <td>1.1 MB</td>
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
        <td>Soundex</td>
        <td>119,095</td>
        <td>1.1 MB</td>
        <td>~ 16 MB</td>
        <td>~ 1130 milliseconds</td>
        <td>~ 0.18 milliseconds (yes right!)</td>
        <td>
            <ul>
                <li>For word "hallo"</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Caverphone 1.0</td>
        <td>119,095</td>
        <td>1.1 MB</td>
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
        <td>1.1 MB</td>
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
        <td>1.1 MB</td>
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
This package is still in an early version and would love to have your contributions!

## 📝 References

- https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.2138&rep=rep1&type=pdf
- https://scholar.harvard.edu/jfeigenbaum/software/editex
- https://github.com/J535D165/FEBRL-fork-v0.4.2/blob/master/stringcmp.py
- https://caversham.otago.ac.nz/files/working/ctp060902.pdf
- https://en.wikipedia.org/wiki/Caverphone
- https://ieeexplore.ieee.org/document/8257147
- https://www.semanticscholar.org/paper/Edit-distance-weighting-modification-using-phonetic-Ahmad-Indrayana/0d74db8a20f7b46b98c2c77750b9b973a3e4a7b2
- https://nlp.stanford.edu/IR-book/html/htmledition/phonetic-correction-1.html
- http://stevehanov.ca/blog/?id=114
