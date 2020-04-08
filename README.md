# Phoneme Spell Checker Project

## Introduction

This project is a continuation of the work first started by Elsa Thiaville. The aim of this work is to establish if a phoneme based approach to spelling correction can result in corrections that are not picked up by traditional spelling checker tools. An example of a phonetic misspelling is the word 'situation' written by a user as ‘sichweshen'.
Looking at the phoneme sequences for the correct spelling of the word and the incorrect phonetic spelling of the word below:

* sichweshen - S IH CH W EH SH AH N
* situation - S IH CH UW EY SH AH N

We can see from the above that although the word difference by edit distance is vastly different (7 operations), the phoneme sequence is not very different at all (2 edits). However, there is a better way to measure phoneme sequence edit distance rather than using the traditional insert, delete, transpose, replace of traditional edit distance methods. Instead we can measure the similarity or dissimilarity based on *acoustic similarity*. To do achieve this, Emma O'Neil's work on phoneme edit distance and acoustic similarity was used in this project. Using this edit distance work, the two above phoneme sequences achieve an acoustic similarity edit distance of *0.27*, much closer, and a good match for the correct word and the attempted spelling.

This initial study focuses purely on the correction of individual misspellings. It does not take into account the word context in a given sentence and does not cover other errors such as grammatical or malapropisms. 

## Methodology 

### How the Phoneme Sequence Spelling Corrector Works

1. Misspellings are gathered as a word list which is passed to the [CMU Sequence-to-Sequence G2P toolkit](https://github.com/cmusphinx/g2p-seq2seq) for conversion into phoneme sequences.
2. The resulting list of phonemes is structured into a Python dictionary for the dataset and method for easy access, lookup and corrections. 
3. A fork of SymSpell is used, which instead of running symmetric delete operations on character strings (words), it works for phoneme sequences. This generates a candidate list of phoneme sequences for quick lookup and edit distance calculation.
4. The acoustic edit distances of the candidate sequences is calculated against the matching entries in the [CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict). Results are scored by distance and then word frequency. The frequency values are taken from the SymSpell frequency dictionary found [here](https://raw.githubusercontent.com/wolfgarbe/SymSpell/master/SymSpell.FrequencyDictionary/en-80k.txt).
5. The top result from the CMU dictionary is found and the resulting word returned and added to the dictionary item as the suggested correction.
 

### Tools

For comparison with the phoneme sequence spelling corrector, two Python spell checker tools were used. These are:

* [PySpellChecker](https://pypi.org/project/pyspellchecker/) - and implementation of [Peter Norvig's](https://norvig.com/spell-correct.html) spelling corrector.
* [SymSpell](https://github.com/wolfgarbe/SymSpell) - a symmetric delete spell checker built for speed.

PySpellChecker - Generates all possible terms for a word with an edit distance (deletes + transposes + replaces + inserts) from the query term and then searches in the dictionary. 

SymSpell – Generates terms with an edit distance (deletes only) from the dictionary, and then adds these terms along with the original term to the dictionary.

### Datasets of Misspellings

A total of five corporas of misspellings were used. Four of these were publicly available, the fifth was provided by an educational company.

Publicly available corpora from [Birkbeck University of London](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html):

* Birkbeck – 36,133 misspellings of 6,136 words. Errors amalgamated from native-speaker section of the Birkbeck spelling corpus. Includes results of spelling tests and errors from free writing taken mostly from schoolchildren, university students or adult literacy students.
* Holbrook – 1,791 misspellings of 1,200 words. Extracts of writings of secondary-school children in their penultimate year of school.
* Aspell – 531 misspellings of 450 words. Used for testing GNU Aspell spellchecker.
* Wikipedia – 2,455 misspellings of 1,922 words. List of misspellings made by Wikipedia editors

Data provided by [Zeeko](https://zeeko.ie), a bullying education company in Nova UCD: 

* Zeeko Dataset – 232 misspellings of 163 words. Gathered from 15 Zeeko surveys carried out by school children in Ireland. Free-text field input on a submitted survey. Due to it being submitted the dataset may be more susceptible to typos (keyboard strokes) or auto corrects.
* Misspellings were hand labelled by referencing the context of the misspelling and interpreting the presumed correct spelling.
* Where a judgment could not be made, the misspelling was excluded from the dataset.

### Preprocessing 



## Results

All accuracy and overlap results for each dataset using each of the three methods (SymSpell, PySpellChecker and CMU Phoneme sequence) can be seen in the Jupyter Notebook [results_spelling_correction_overlap_and_scores.ipynb](https://github.com/robertyoung2/nlp_phoneme_spelling/blob/master/data_analysis/results_spelling_correction_overlap_and_scores.ipynb)

To view the word corrections for each dataset and comparison method, navigate to the folder [results](https://github.com/robertyoung2/nlp_phoneme_spelling/tree/master/data_analysis/results). This is broken down by:

* Dataset eg. Birkbeck, Aspell, Zeeko, Holbrook, Wikipedia.
* Within each dataset is a sub-directory of the compared methods. For example, for the dataset birkbeck, comparing SymSpell against the CMU Phonemes method you would go to [/results/birkbeck/symspell_cmu_phonemes/](https://github.com/robertyoung2/nlp_phoneme_spelling/tree/master/data_analysis/results/birkbeck/symspell_cmu_phonemes). In here there are three csv file which show the words corrected by both methods, and the unique word corrections by one or other methods.

## Set up

## Input Files

## G2P Files

## Key Scripts



