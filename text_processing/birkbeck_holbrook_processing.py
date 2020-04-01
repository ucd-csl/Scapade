from pathlib import Path
import pickle
import pkg_resources
import pandas as pd
from spellchecker import SpellChecker
from symspellpy_words import SymSpell, Verbosity
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes


# input_path_files = "C:/Users/robert/Documents/zeeko_nlp/input_files/" # path format windows
# output_path_files = "C:/Users/robert/Documents/zeeko_nlp/input_files/spelling_correction_dicts"
output_path_files = "/Users/robertyoung/git_repos/nlp_phoneme_spelling/input_files/spelling_correction_dicts"
input_path_files = "/Users/robertyoung/git_repos/nlp_phoneme_spelling/input_files/" # path format mac
birkbeck_mispellings_path = Path(input_path_files) / 'birkbeck.txt'
holbrook_mispellings_path = Path(input_path_files) / 'holbrook-missp.txt'


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
    output_path = "C:/Users/robert/Documents/zeeko_nlp/g2p_files/"
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
    input_path = "C:/Users/robert/Documents/zeeko_nlp/g2p_files/"
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

    input_path_files = "C:/Users/robert/Documents/zeeko_nlp/input_files/spelling_correction_dicts"
    dataset = dataset + "_phonemes_dict.txt"
    phonemes_dict = Path(input_path_files) / dataset
    phonemes_dict = pickle.load(open(phonemes_dict, "rb"))

    input_path_csv = Path("C:/Users/robert/Documents/zeeko_nlp/input_files/") / "cmu_frequency.csv"
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


def main():
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    sym_spell = create_sym_object()
    #
    # birkbeck_template = create_default_dict(birkbeck_mispellings_path)
    # pickle_output(birkbeck_template, 'birkbeck_template_dict.txt')
    # g2p_word_list(birkbeck_template, 'birkbeck_word_list.txt')
    # birkbeck_sym = symspell_dict('holbrook', sym_spell)
    # pickle_output(birkbeck_sym, 'birkbeck_symspell_dict.txt')
    # birkbeck_phonemes = add_phonemes(birkbeck_template, 'birkbeck')
    # pickle_output(birkbeck_phonemes, 'birkbeck_phonemes_dict.txt')

    holbrook_template = create_default_dict(holbrook_mispellings_path)
    pickle_output(holbrook_template, 'holbrook_template_dict.txt')
    # g2p_word_list(holbrook_template, 'holbrook_word_list.txt')
    holbrook_sym = symspell_dict('holbrook', sym_spell)
    pickle_output(holbrook_sym, 'holbrook_symspell_dict.txt')
    # holbrook_phonemes = add_phonemes(holbrook_template, 'holbrook')
    # pickle_output(holbrook_phonemes, 'holbrook_phonemes_dict.txt')
=======
=======
>>>>>>> Stashed changes

    # sym_spell = create_sym_object()

    birkbeck_template = create_default_dict(birkbeck_mispellings_path)
    pyspell_dict(birkbeck_template, 'birkbeck')
    # pickle_output(birkbeck_template, 'birkbeck_template_dict.txt')
    # g2p_word_list(birkbeck_template, 'birkbeck_word_list.txt')
    # birkbeck_sym = symspell_word_dict('holbrook', sym_spell)
    # pickle_output(birkbeck_sym, 'birkbeck_symspell_dict.txt')
    # birkbeck_phonemes = add_phonemes(birkbeck_template, 'birkbeck')
    # pickle_output(birkbeck_phonemes, 'birkbeck_phonemes_dict.txt')
    # birkbeck_phonemes_sym = symspell_phonemes('TOP', 'birkbeck')
    # pickle_output(birkbeck_phonemes_sym, 'birkbeck_phonemes_sym.txt')

    # holbrook_template = create_default_dict(holbrook_mispellings_path)
    # pyspell_dict(holbrook_template, 'holbrook')
    # pickle_output(holbrook_template, 'holbrook_template_dict.txt')
    # g2p_word_list(holbrook_template, 'holbrook_word_list.txt')
    # holbrook_sym = symspell_word_dict('holbrook', sym_spell)
    # pickle_output(holbrook_sym, 'holbrook_symspell_dict.txt')
    # holbrook_phonemes = add_phonemes(holbrook_template, 'holbrook')
    # pickle_output(holbrook_phonemes, 'holbrook_phonemes_dict.txt')
    # holbrook_phonemes_sym = symspell_phonemes('TOP', 'holbrook')
    # pickle_output(holbrook_phonemes_sym, 'holbrook_phonemes_sym.txt')
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes


if __name__ == "__main__":
    main()
