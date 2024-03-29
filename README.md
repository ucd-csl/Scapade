# S-capade - Acoustic Similarity Spelling Correction 

## Table of Contents

1. [Introduction](#introduction) <br/>
2. [Methodology](#methodology) <br/>
    2.1 [How S-capade Works](#how_works) <br/>
    2.2 [Tools](#tools) <br/>
    2.3 [Datasets of Misspellings](#misspellings) <br/>
    2.4 [Preprocessing](#preprocessing) <br/>
3. [Results](#results) <br/>
    3.1 [Scores and Overlap Results Notebook](#results_scores_overlap) <br/>
    3.2 [Word Corrections Using Phoneme Method](#results_word_corrections) <br/>
4. [Word List to Phoneme Sequence - G2P](#g2p_update) <br/>
5. [Other Folder Information](#other_folders) <br/>
    5.1 [input_files/](#input_files) <br/>
    5.2 [input_files/spelling_correction_dicts/](#spell_dicts) <br/>
    5.3 [g2p_files/](#g2p_files) <br/>
    5.4 [symspellpy_scapade/](#symspell_scapade) <br/>
6. [Known Issues and Future Work](#issues_and_future) <br/>
    6.1 [Known Issues](known_issues) <br/>
    6.2 [Future Work](future_work) <br/>
7. [Requirements](#requirements) <br/>


## 1.0 - Introduction <a name="introduction"></a>

This project is a continuation of the work first started by Elsa Thiaville. The aim of this work is to establish if a phoneme based approach to spelling correction can result in corrections that are not picked up by traditional spelling checker tools. An example of a phonetic misspelling is the word 'situation' written by a user as ‘sichweshen'.
Looking at the phoneme sequences for the correct spelling of the word and the incorrect phonetic spelling of the word below:

* sichweshen - S IH CH W EH SH AH N
* situation - S IH CH UW EY SH AH N

We can see from the above that although the word difference by edit distance is vastly different (7 operations), the phoneme sequence is not very different at all (2 edits). However, there is a better way to measure phoneme sequence edit distance rather than using the traditional insert, delete, transpose, replace of traditional edit distance methods. Instead we can measure the similarity or dissimilarity based on *acoustic similarity*. To do achieve this, Emma O'Neil's work on phoneme edit distance and acoustic similarity was used in this project. Using this edit distance work, the two above phoneme sequences achieve an acoustic similarity edit distance of **1.10**, much closer, and a good match for the correct word and the attempted spelling.

This initial study focuses purely on the correction of individual misspellings. It does not take into account the word context in a given sentence and does not cover other errors such as grammatical or malapropisms. 

To view a simple example of S-capade working for phoneme representations of misspellings, please use the notebook [
S-capade Single Phoneme Sequence Correction Demo](https://github.com/ucd-csl/Scapade/blob/master/S-capade%20Single%20Phoneme%20Sequence%20Correction%20Demo.ipynb).

## 2.0 - Methodology <a name="methodology"><a/>

### 2.1 - How S-capade Works <a name="how_works"><a/>

1. Misspellings are gathered as a word list which is passed to the [CMU Sequence-to-Sequence G2P toolkit](https://github.com/cmusphinx/g2p-seq2seq) for conversion into phoneme sequences.
2. The resulting list of phonemes is structured into a Python dictionary for the dataset and method for easy access, lookup and corrections. 
3. A fork of SymSpell is created and used, which instead of running symmetric delete operations on character strings (words), it works for phoneme sequences. This generates a candidate list of phoneme sequences for quick lookup and edit distance calculation.
4. The acoustic edit distances of the candidate sequences is calculated against the matching entries in the [CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict). Results are scored by distance and then word frequency. The frequency values are taken from the SymSpell frequency dictionary found [here](https://raw.githubusercontent.com/wolfgarbe/SymSpell/master/SymSpell.FrequencyDictionary/en-80k.txt).
5. The top result from the CMU dictionary is found and the resulting word returned and added to the dictionary item as the suggested correction.
 

### 2.2 - Tools <a name="tools"><a/>

For comparison with the S-capade sequence spelling corrector, three spell checker tools were used. These are:

* [PySpellChecker](https://pypi.org/project/pyspellchecker/) - an implementation of [Peter Norvig's](https://norvig.com/spell-correct.html) spelling corrector.
* [SymSpell](https://github.com/wolfgarbe/SymSpell) - a symmetric delete spell checker built for speed.
* [GNU Aspell](http://aspell.net/) - free and Open Source spell checker. 

PySpellChecker - Generates all possible terms for a word with an edit distance (deletes + transposes + replaces + inserts) from the query term and then searches in the dictionary. 

SymSpell – Generates terms with an edit distance (deletes only) from the dictionary, and then adds these terms along with the original term to the dictionary.

Aspell - standard spell checker for the GNU operating system. It also compiles for other Unix-like operating systems and Windows.

### 2.3 - Datasets of Misspellings <a name="misspellings"></a>

A total of five corporas of misspellings were used. Four of these were publicly available, the fifth was provided by an educational company.

Publicly available corpora from [Birkbeck University of London](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html):

* **Birkbeck** – 36,133 misspellings of 6,136 words. Errors amalgamated from native-speaker section of the Birkbeck spelling corpus. Includes results of spelling tests and errors from free writing taken mostly from schoolchildren, university students or adult literacy students.
* **Holbrook** – 1,791 misspellings of 1,200 words. Extracts of writings of secondary-school children in their penultimate year of school.
* **Aspell** – 531 misspellings of 450 words. Used for testing GNU Aspell spellchecker.
* **Wikipedia** – 2,455 misspellings of 1,922 words. List of misspellings made by Wikipedia editors

Data provided by [Zeeko](https://zeeko.ie), a bullying education company in Nova UCD: 

* **Zeeko Dataset** – 232 misspellings of 163 words. Gathered from 15 Zeeko surveys carried out by school children in Ireland. Free-text field input on a submitted survey. Due to it being submitted the dataset may be more susceptible to typos (keyboard strokes) or auto corrects.
* Misspellings were hand labelled by referencing the context of the misspelling and interpreting the presumed correct spelling.
* Where a judgment could not be made, the misspelling was excluded from the dataset.

### 2.4 - Preprocessing <a name="preprocessing"><a/>

The scripts to pre-processing the input data found in [/text_processing/](https://github.com/ucd-csl/Scapade/tree/master/text_processing) are as follows:

* [dataset_processing.py](https://github.com/ucd-csl/Scapade/blob/master/text_processing/cmu_preprocess.py) - Preprocesses each dataset creating the required word list for g2p and corresponding dictionary objects for each spelling tool to use as input and output.
* [cmu_preprocess.py](https://github.com/ucd-csl/Scapade/blob/master/text_processing/cmu_preprocess.py) - Updates the CMU dictionary to contain frequencies for each word from the SymSpell word dictionary.
* [valid_word_process.py](https://github.com/ucd-csl/Scapade/blob/master/text_processing/valid_word_process.py) - Creates a list of valid words that the enchant dictionary does no recognised. Used to ensure only spelling mistakes are extracted from the Zeeko dataset, not valid but unrecognised words such as 'Snapchat'.
* [/zeeko_survey_spelling_extraction.py](https://github.com/ucd-csl/Scapade/blob/master/text_processing/zeeko_survey_spelling_extraction.py) - Extracts the spelling mistakes from all 15 Zeeko surveys.

## 3.0 - Results <a name="results"><a/>

### 3.1 - Scores and Overlap Results Notebook <a name="results_scores_overlap"><a/>

All accuracy and overlap results for each dataset using each of the four methods (SymSpell, PySpellChecker, Aspell and the Phoneme sequence) can be seen in the Jupyter Notebook [Results.ipynb](https://github.com/ucd-csl/Scapade/blob/master/data_analysis/Results.ipynb)

### 3.2 - Word Corrections Using S-capade Method <a name="results_word_corrections"><a/>

A notebook linking to all of the word correction results for the S-capade method across the datasets using SymSpell as the comparison method can be seen in [Corrected-Words.md](https://github.com/ucd-csl/Scapade/blob/master/data_analysis/Corrected-Words.md).

To view the word corrections for each dataset and comparison method, navigate to the folder [results](https://github.com/ucd-csl/Scapade/tree/master/data_analysis/results). This is broken down by:

* Dataset eg. Birkbeck, Aspell, Zeeko, Holbrook, Wikipedia.
* Within each dataset is a sub-directory of the compared methods. For example, for the dataset birkbeck, comparing SymSpell against the S-capade method you would go to [/results/birkbeck/symspell_vs_scapade/](https://github.com/ucd-csl/Scapade/tree/master/data_analysis/results/birkbeck/symspell_vs_scapade). In here there are three csv file which show the words corrected by both methods, and the unique word corrections by one or other methods.

## 4.0 - Word List to Phoneme Sequence - G2P <a name="g2p_update"><a/>

In the shell script [g2p_word_list.sh](https://github.com/ucd-csl/Scapade/tree/master/shell_scripts), please edit this script with your correct G2P model path on line 4.

## 5.0 - Other Folder Information <a name="other_folders"><a/>

### 5.1 - [input_files/](https://github.com/ucd-csl/Scapade/tree/master/input_files) <a name="input_files"><a/>

All required input files for the scripts to operate are placed here. These include:
* The text files of misspellings to be processed eg. [holbrook-missp.txt](https://github.com/ucd-csl/Scapade/blob/master/input_files/holbrook-missp.txt)

### 5.2 - [input_files/spelling_correction_dicts/](https://github.com/ucd-csl/Scapade/tree/master/input_files/spelling_correction_dicts) <a name="spell_dicts"><a/>

Contains all the dictionaries with the suggested corrections from each dataset for each method. Used to obtain and compare the results. 

### 5.3 - [g2p_files/](https://github.com/ucd-csl/Scapade/tree/master/g2p_files) <a name="g2p_files"><a/>

This contains the input and output for the g2p script which converts word lists into their phoneme representation.

Example input word list - [aspell_word_list.txt](https://github.com/ucd-csl/Scapade/blob/master/g2p_files/aspell_word_list.txt)
Example output word-phoneme list - [aspell_phonemes.txt](https://github.com/ucd-csl/Scapade/blob/master/g2p_files/aspell_phonemes.txt)

### 5.4 - [symspellpy_scapade](https://github.com/ucd-csl/Scapade/tree/master/symspellpy_scapade) <a name="symspell_scapade"><a/>

This folder contains the core code for S-capade. It uses an adapted version of SymSpell/SymSpellPy to generate the potential delete candidates (speed, to avoid doing exhaustive search look up). This means on average it's about 2-3 seconds per word look up and candidate list generation. Key files in here for the project to function:

* The acoustic spelling distance matrix - [acoustic_distributional_distance_matrix.csv](https://github.com/ucd-csl/Scapade/blob/master/symspellpy_scapade/distance_matrix_spelling_correction.csv)
* The CMU Pronunciation dictionary with word frequencies - [https://github.com/ucd-csl/Scapade/blob/master/symspellpy_scapade/cmu_frequency_added.csv](https://github.com/ucd-csl/Scapade/blob/master/symspellpy_scapade/cmu_frequency_added.csv)

## 6.0 Known Issues and Future Work <a name="issues_and_future"><a/>

### 6.1 Known Issues <a name="known_issues"><a/>

* ~~Re-run Birkbeck dataset with corrected implementation~~ - _Birkbeck dataset processed_.
* ~~Improve speed performance of lookups (currently disabled as not working 100% as intended)~~ - _changed edit distance from 3 to 2._
* ~~Currently each benchmarked method (PySpell, SymSpell, Aspell, S-capade Method) all use their own custom dictionary. Creation and extension of a common lookup and generation dictionary is required to ensure all methods are using the same list of words.~~ Data processing steps now adds missing words to each dictionary for each tool. 
* ~~Requires comparison against a phonetic spell checker, such as Aspell.~~ - _Aspell comparison now implemented in results._

### 6. 2 Future Work <a name="future_work"><a/>

* Explore re-training g2p tool on misspellings to see if it results in an improvement in predicting phonemic representations. Need to investigate data to use and how this impacts generalisation of the model.
* Investigate distance measure decrease between predicted phoneme sequence and target phoneme sequence. For example: stopping will be predicted as "S T OW P IH NG", but the distance between OW and AA (correct phoneme) will be reduced. This could be done by tuning the matrix to the speaker accent, or may need a new matrix trained on possible pronunciation of letters.
* Create unit testing suite. 
* Improve the overall performance (time complexity) of the tool. Alphabet contains 26 letters, CMU phonemes contain 39 phonemes. Standard spelling correction dictionaries contain ~90,000 words, CMU dictionary has ~134,000 words. These two points mean that candidate generation using the symmetric delete approach run on average ~3 seconds per candidate generation. Strategies could be devised to improve this lookup time. One example could be to reduce the size of the CMU dictionary so that it only contained valid, commonly used words like other standard dictionaries. This would reduce the permutations of delete candidates to compare distances with. 
* Explore using a language model to correct misspellings in context.
* Find a way to integrate g2p into Scapade to make it more seamless and remove this misspelling preparation step. 

## 7.0 Requirements

Requirements can be installed using pip and the provided 'requirements.txt' file. For g2p-seq2seq to run correctly you will need to ensure the following:
* Python version no greater than 3.7 (tensorflow legacy install required)
* tensorflow == 1.15
* tensor2tensor == 1.7
* [g2p-seq2seq](https://github.com/cmusphinx/g2p-seq2seq)
* To run aAspell-python spell checker on the datasets, there are a couple of install steps required. See the GitHuh [repo](https://github.com/WojciechMula/aspell-python) for more details.