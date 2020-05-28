import pickle
import os.path
import pandas as pd
from spellchecker import SpellChecker
import aspell as ap

# load in misspelling datasets
file_path = '../input_files/'
aspell = file_path + 'aspell.txt'
birkbeck = file_path + 'birkbeck.txt'
holbrook = file_path + 'holbrook-missp.txt'
wikipedia = file_path + 'wikipedia.txt'
zeeko = file_path + 'zeeko_misspellings.txt'
output_file = '../spelling_mistakes/' + 'target_words_all.txt'
datasets = {'aspell': aspell, 'birkbeck': birkbeck, 'holbrook': holbrook, 'wikipedia': wikipedia, 'zeeko': zeeko}

# load in dictionaries for each tool

cmu_dict = '../symspellpy_phonemes/cmu_frequency.csv'
symspell_words = '../symspellpy_words/frequency_dictionary_en_82_765.txt'
target_words = list(pickle.load(open(output_file, 'rb')))


def get_targets():
    # get all the target misspellings for each dataset and store these as lower case words in a set
    if not os.path.exists(output_file):
        all_set = set()
        for key, value in datasets.items():
            with open(datasets[key], 'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    if line[0] == '$' and '_' not in line:
                        all_set.add(line[1:].lower())

        pickle.dump(all_set, open(output_file, 'wb'))


def missing_targets_cmu(cmu_dict, target_words):
    df_cmu = pd.read_csv(cmu_dict)
    all_words = (df_cmu.iloc[:, 0].tolist())
    all_words = set(all_words)
    missing_words = set()
    for word in target_words:
        if word not in all_words:
            missing_words.add(word)
    missing_words = list(missing_words)

    with open('../g2p_files/cmu_missing_targets.txt', 'w') as missing_words_file:
        for word in missing_words:
            missing_words_file.write(word)
            missing_words_file.write("\n")


def missing_targets_sym(symspell_words, target_words):

    with open(symspell_words, 'r') as f:
        lines = f.read().splitlines()
        sym_spell_all = []
        missing_words = set()
        for line in lines:
            current_word = line.split()[0].lower()
            sym_spell_all.append((current_word))

        for word in target_words:
            if word not in sym_spell_all:
                missing_words.add(word)

    missing_words = list(missing_words)
    with open('../spelling_mistakes/symspell_missing_targets.txt', 'w') as sym_missing:
        for word in missing_words:
            new_line = word + ' 1' + '\n'
            sym_missing.write(new_line)


def missing_targets_aspell(target_words):
    s = ap.Speller('lang', 'en')
    missing_words = set()
    for word in target_words:
        if s.check(word) == False:
            missing_words.add(word)
    missing_words = list(missing_words)

    with open('../spelling_mistakes/aspell_missing_targets.txt', 'w') as aspell_misspelling:
        for word in missing_words:
            new_line = word + '\n'
            aspell_misspelling.write(new_line)


def missing_targets_pyspell(target_words):
    spell = SpellChecker()
    misspelled = spell.unknown(target_words)

    with open('../spelling_mistakes/pyspell_missing_targets.txt', 'w') as pyspell_misspelling:
        for word in misspelled:
            new_line = word + '\n'
            pyspell_misspelling.write(new_line)


missing_targets_cmu(cmu_dict, target_words)
missing_targets_sym(symspell_words, target_words)
missing_targets_aspell(target_words)
missing_targets_pyspell(target_words)