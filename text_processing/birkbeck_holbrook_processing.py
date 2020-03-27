from pathlib import Path
from spellchecker import SpellChecker
import pkg_resources
from symspellpy import SymSpell, Verbosity
import pickle

input_path_files = "C:/Users/robert/Documents/zeeko_nlp/input_files/" # path format windows
output_path_files = "C:/Users/robert/Documents/zeeko_nlp/input_files/spelling_correction_dicts"
# path_files = "/Users/robertyoung/git_repos/nlp_phoneme_spelling/input_files/" # path format mac
birkbeck_mispellings_path = Path(input_path_files) / 'birkbeck.txt'
holbrook_mispellings_path = Path(input_path_files) / 'holbrook-missp.txt'


def create_sym_object():
    sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=15)
    dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    return sym_spell


def create_default_dict(file_path):

    dictionary_template = {}
    with open(file_path) as data_source:
        lines = [line.rstrip()for line in data_source]
        for line in lines:
            line = line.split()[0]
            if line[0] == '$':
                correct_spelling = line[1:].lower()
                continue
            mispelling = line.lower()
            dictionary_template[mispelling] = {'correct_spelling':correct_spelling}

    return dictionary_template


def symspell_dict(input_dict, sym_spell):
    working_dict = input_dict.copy()

    for misspelling, details in working_dict.items():
        input_term = misspelling
        suggestion = sym_spell.lookup(input_term, Verbosity.CLOSEST, max_edit_distance=2)
        suggestions = []

        if len(suggestion) == 0:
            working_dict[misspelling]['suggested'] = ""
            working_dict[misspelling]['candidates'] = ""
        if len(suggestion) == 1:
            working_dict[misspelling]['suggested'] = str(suggestion[0]).split(',')
            working_dict[misspelling]['candidates'] = ""
        if len(suggestion) > 1:
            for symspell_suggest in suggestion:
                suggestions.append(str(symspell_suggest).split(','))
            working_dict[misspelling]['suggested'] = suggestions[0]
            working_dict[misspelling]['candidates'] = suggestions

    return working_dict


def pyspell_dict(input_dict):
    spell = SpellChecker()
    working_dict = input_dict.copy()

    for mispelling, details in working_dict.items():

        # Get the one `most likely` answer
        working_dict[mispelling]['correction'] = spell.correction(mispelling)

        # Get a list of `likely` options
        working_dict[mispelling]['candidates'] = spell.candidates(mispelling)


def pickle_output(dict_object, name):
    path = Path(output_path_files) / name
    pickle.dump(dict_object, open(path, "wb"))


def main():

    sym_spell = create_sym_object()

    birkbeck_template = create_default_dict(birkbeck_mispellings_path)
    birkbeck_sym = symspell_dict(birkbeck_template, sym_spell)
    pickle_output(birkbeck_sym, 'birkbeck_symspell_dict.txt')

    holbrook_template = create_default_dict(holbrook_mispellings_path)
    holbrook_sym = symspell_dict(holbrook_template, sym_spell)
    pickle_output(holbrook_sym, 'holbrook_symspell_dict.txt')


if __name__ == "__main__":
    main()




