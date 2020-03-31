from pathlib import Path
from spellchecker import SpellChecker
import pkg_resources
from symspellpy_words import SymSpell, Verbosity
import pickle

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


def symspell_dict(name, sym_spell):
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


def pyspell_dict(input_dict):
    spell = SpellChecker()
    working_dict = input_dict.copy()
    for mispelling, details in working_dict.items():
        working_dict[mispelling]['correction'] = spell.correction(mispelling)
        working_dict[mispelling]['candidates'] = spell.candidates(mispelling)


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


def pickle_output(dict_object, name):
    path = Path(output_path_files) / name
    pickle.dump(dict_object, open(path, "wb"))


def main():
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


if __name__ == "__main__":
    main()
