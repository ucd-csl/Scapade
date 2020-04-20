import subprocess, time
from sys import platform
from pathlib import Path
import pickle
import pkg_resources
import pandas as pd
from spellchecker import SpellChecker
from symspellpy_words import SymSpell, Verbosity


input_path_files = "../input_files/"
output_path_files = "../input_files/spelling_correction_dicts"

birkbeck_mispellings_path = Path(input_path_files) / 'birkbeck.txt'
holbrook_mispellings_path = Path(input_path_files) / 'holbrook-missp.txt'
zeeko_mispellings_path = Path(input_path_files) / 'zeeko_misspellings.txt'
aspell_mispellings_path = Path(input_path_files) / 'aspell.txt'
wiki_mispellings_path = Path(input_path_files) / 'wikipedia.txt'

dataset_paths = {'birkbeck':birkbeck_mispellings_path, 'holbrook':holbrook_mispellings_path,
                 'zeeko':zeeko_mispellings_path, 'aspell':aspell_mispellings_path, 'wiki':wiki_mispellings_path}

def create_sym_object():
    """
    Initiates symspell phonemes object for use in lookup
    :return: sym_spell
    """

    sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=15)
    dictionary_path = pkg_resources.resource_filename("symspellpy_words", "frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)


    return sym_spell


def create_default_dict(file_path):
    """
    Creates a default dictionary Python object for the provided dataset
    :param file_path: the file path that points to the input dataset
    :return: Python dictionary template for the dataset
    """

    dictionary_template = {}
    with open(file_path) as data_source:
        lines = [line.rstrip()for line in data_source]
        for line in lines:
            line = line.split()[0]
            if line[0] == '$':
                if '_' in line:
                    correct_spelling = 'skip'
                    continue
                correct_spelling = line[1:].lower()
                continue
            if correct_spelling != 'skip':
                misspelling = line.lower()
                dictionary_template[misspelling] = {'correct_spelling':correct_spelling}

    return dictionary_template


def g2p_word_list(template_dict, name):
    """
    Creates a file of words, each on a new line, to pass to g2p
    :param template_dict: Python template dictionary for the provided dataset
    :param name: name of the word list to write to
    :return: None
    """
    output_path = "../g2p_files/"
    file_name = Path(output_path) / name
    with open(file_name, 'w') as file:
        for key, value in template_dict.items():
            key = key.replace('_', '')
            file.write(key+"\n")


def g2p_phoneme_list(dataset_name):
    """
    Calls the shell script which executes g2p, converting a list of words into a list of words with their phoneme
    representation
    :param dataset_name: dataset to execute in g2p eg. "zeeko"
    :return: None.
    """
    if platform == "win32":
        subprocess.check_call(["C:\Program Files\Git\git-bash.exe",
                          "../shell_scripts/g2p_word_list.sh", dataset_name])
    else:
        subprocess.check_call(["../shell_scripts/g2p_word_list.sh", dataset_name])


def symspell_word_dict(dataset_name, sym_spell):
    """
    Adds suggested correction using symspell to the provided dictionary
    :param name: Name of the dataset to be added to output file
    :param sym_spell: sym_spell object
    :return:
    """
    name = dataset_name + "_template_dict.txt"
    full_path = Path(output_path_files) / name
    working_dict = pickle.load(open(full_path, "rb"))
    for misspelling, details in working_dict.items():
        input_term = misspelling.replace("_", " ")
        suggestion = sym_spell.lookup(input_term, Verbosity.CLOSEST, max_edit_distance=2)
        suggestions = []

        if len(suggestion) == 0:
            working_dict[misspelling]['suggested'] = ""
            working_dict[misspelling]['candidates'] = ""
        if len(suggestion) == 1:
            working_dict[misspelling]['suggested'] = str(suggestion[0]).split(',')[0]
            working_dict[misspelling]['candidates'] = ""
        if len(suggestion) > 1:
            for symspell_suggest in suggestion:
                suggestions.append(str(symspell_suggest).split(',')[0])
            working_dict[misspelling]['suggested'] = suggestions[0]
            working_dict[misspelling]['candidates'] = suggestions

    return working_dict


def pyspell_dict(input_dict, name):
    """
    Adds suggested corrections to provided dictionary
    :param input_dict: input dictionary template
    :param name: name of dataset for use in file output write
    :return: None
    """
    file_name = name + "_pyspell_dict.txt"
    spell = SpellChecker()
    working_dict = dict(input_dict)
    counter = 0
    for mispelling, details in working_dict.items():
        if counter % 100 == 0:
            print(counter)
        working_dict[mispelling]['suggested'] = spell.correction(mispelling)
        working_dict[mispelling]['candidates'] = list(spell.candidates(mispelling))
        counter += 1

    return working_dict, file_name


def add_phonemes(input_dict, name):
    """
    Adds phoneme representation of misspelling to provided dictionary
    :param input_dict: Input template dictionary
    :param name: name of the input phoneme list to read from
    :return: Updated dictionary with phoneme rep of misspellings added
    """
    input_path = "../g2p_files/"
    file_name = name + "_phonemes.txt"
    file = Path(input_path) / file_name
    current_dict = input_dict.copy()
    keys_order = []
    for keys in current_dict.keys():
        keys_order.append(keys)

    with open(file, "r") as phonemes_list:
        i = 0
        for line in phonemes_list:
            line = line.rstrip("\n").split(" ", 1)
            word, phoneme = line[0], line[1]
            current_dict[keys_order[i]]['phoneme_rep'] = phoneme
            current_dict[keys_order[i]]['suggested'] = ""
            i += 1

    return current_dict


def symspell_phonemes(verbosity_level, dataset):
    """
    Gets suggested word correction for misspelling phoneme representation and updates the dictionary with the
    suggested corrections
    :param verbosity_level: What level of correction and return required. TOP, CLOSE, ALL. See symspell code
    editdistance.py
    :param dataset: Which dictionary dataset to write to.
    :return:
    """
    from symspellpy_phonemes import symspellpy
    SymSpell = symspellpy.SymSpell
    Verbosity = symspellpy.Verbosity

    sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=15)
    dictionary_path = pkg_resources.resource_filename("symspellpy_phonemes", "cmu_frequency.csv")
    sym_spell.load_dictionary(dictionary_path, term_index=1, count_index=2)

    input_path_files = "../input_files/spelling_correction_dicts"
    dataset = dataset + "_phonemes_dict.txt"
    phonemes_dict = Path(input_path_files) / dataset
    phonemes_dict = pickle.load(open(phonemes_dict, "rb"))

    input_path_csv = Path("../input_files/") / "cmu_frequency.csv"
    df = pd.read_csv(input_path_csv, names=['word', 'seq', 'count'])
    counter = 0
    for key in phonemes_dict.keys():
        if counter % 10 == 0:
            print('Iteration number:', counter)
        input_term = phonemes_dict[key]['phoneme_rep']

        if verbosity_level == 'TOP':
            suggestions = sym_spell.lookup(input_term, Verbosity.TOP)
        elif verbosity_level == 'CLOSEST':
            suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST)
        else:
            suggestions = sym_spell.lookup(input_term, Verbosity.ALL)

        phonemes_dict[key]['candidates'] = []
        for suggestion in suggestions:
            if len(phonemes_dict[key]['candidates']) >= 10:
                break
            current_seq = str(suggestion).split(',')[0]
            df_slice = df[df['seq'] == current_seq].sort_values(by=['count'], ascending=False)
            if phonemes_dict[key]['suggested'] == '' and df_slice.iloc[0]['count'] > 1:
                phonemes_dict[key]['suggested'] = df_slice.iloc[0]['word']
                phonemes_dict[key]['suggested_phoneme'] = str(suggestion).split(',')[0]
                print(phonemes_dict[key]['correct_spelling'],phonemes_dict[key]['suggested'])
            if len(phonemes_dict[key]['suggested']) > 0 and len(phonemes_dict[key]['candidates']) <= 10:
                df_slice = df_slice[df_slice['count'] > 1]
                phonemes_dict[key]['candidates'] += (list(df_slice[:5]['word']))
        counter += 1

    return phonemes_dict


def pickle_output(dict_object, name):
    """
    Pickle dump the Python object
    :param dict_object: dictionary to be serialised
    :param name: name of the dataset for file writing
    :return: None
    """
    path = Path(output_path_files) / name
    pickle.dump(dict_object, open(path, "wb"))


def process_given_dataset(path_misspellings, dataset_name, sym_spell):
    """
    Calls all the functions in the correct order start to finish to process text, update dicts, and provide results
    :param path_misspellings: The location of misspellings input document
    :param dataset_name: The dataset being used
    :param sym_spell: Passing the SymSpell object
    :return: None
    """
    name_template_dict = dataset_name + "_template_dict.txt"
    name_word_list = dataset_name + "_word_list.txt"
    name_symspell_dict = dataset_name + "_symspell_dict.txt"
    name_phonenems_dict = dataset_name + "_phonemes_dict.txt"
    name_phonemes_sym = dataset_name + "_phonemes_sym.txt"

    template = create_default_dict(path_misspellings)
    pyspell = pyspell_dict(template, dataset_name)
    pickle_output(pyspell[0], pyspell[1])
    pickle_output(template, name_template_dict)
    g2p_word_list(template, name_word_list)
    g2p_phoneme_list(dataset_name)
    sym = symspell_word_dict(dataset_name, sym_spell)
    pickle_output(sym, name_symspell_dict)
    phonemes = add_phonemes(template, dataset_name)
    pickle_output(phonemes, name_phonenems_dict)
    phonemes_sym = symspell_phonemes('TOP', dataset_name)
    pickle_output(phonemes_sym, name_phonemes_sym)


def main():
    sym_spell = create_sym_object()
    data_to_process = ['birkbeck', 'holbrook', 'zeeko', 'aspell', 'wiki']
    for dataset in data_to_process:
        process_given_dataset(dataset_paths[dataset], dataset, sym_spell)


if __name__ == "__main__":
    main()
