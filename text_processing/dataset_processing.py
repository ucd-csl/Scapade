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
    sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=15)
    dictionary_path = pkg_resources.resource_filename("symspellpy_phonemes", "frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    return sym_spell


def create_default_dict(file_path):

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
    output_path = "../g2p_files/"
    file_name = Path(output_path) / name
    with open(file_name, 'w') as file:
        for key, value in template_dict.items():
            key = key.replace('_', '')
            file.write(key+"\n")


def symspell_word_dict(name, sym_spell):
    name = name + "_template_dict.txt"
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

    pickle_output(working_dict, file_name)


def add_phonemes(input_dict, name):
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
        if counter % 100 == 0:
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
            phonemes_dict[key]['suggested_phoneme'] = str(suggestion).split(',')[0]
            current_seq = phonemes_dict[key]['suggested_phoneme']
            df_slice = df[df['seq'] == current_seq].sort_values(by=['count'], ascending=False)
            if phonemes_dict[key]['suggested'] == '':
                phonemes_dict[key]['suggested'] = df_slice.iloc[0]['word']
            if len(df_slice) > 1 and len(phonemes_dict[key]['suggested_phoneme']) < 10:
                phonemes_dict[key]['candidates'] += (list(df_slice[:5]['word']))
        counter += 1

    return phonemes_dict


def pickle_output(dict_object, name):
    path = Path(output_path_files) / name
    pickle.dump(dict_object, open(path, "wb"))


def process_given_dataset(path_mispellings, dataset_name, sym_spell):

    name_template_dict = dataset_name + "_template_dict_1.txt"
    name_word_list = dataset_name + "_word_list_1.txt"
    name_symspell_dict = dataset_name + "_symspell_dict_1.txt"
    name_phonenems_dict = dataset_name + "_phonemes_dict_1.txt"
    name_phonemes_sym = dataset_name + "_phonemes_sym_1.txt"

    template = create_default_dict(path_mispellings)
    pyspell_dict(template, dataset_name)
    pickle_output(template, name_template_dict)
    g2p_word_list(template, name_word_list)
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
