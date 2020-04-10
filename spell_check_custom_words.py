from text_processing import dataset_processing
from pathlib import Path
import os


print("Please enter the name of the dataset in /input_files/. Eg. 'custom.txt'")
user_dataset_name = input("Enter dataset name: ")

input_path_files = "C:/Users/robert/Documents/zeeko_nlp/nlp/"
# output_path_files = "/input_files/spelling_correction_dicts"
# custom_misspellings_path = Path(input_path_files) / user_dataset


dir_path_root = os.path.dirname(os.path.realpath(__file__))
# path_results = Path(dir_path_root) / 'data_analysis' / 'results'
# isFile = os.path.isdir(path_results)
# print(isFile)

def check_make_dir(user_dataset_name):
    path_results = Path(dir_path_root) / 'data_analysis' / 'results'
    path_results_dataset = Path(path_results) / user_dataset_name
    if not os.path.isdir(path_results_dataset):
        os.mkdir(path_results_dataset)
        os.mkdir(Path(path_results_dataset) / 'pyspell_cmu_phonemes')
        os.mkdir(Path(path_results_dataset) / 'symspell_cmu_phonemes')


check_make_dir(user_dataset_name)

def process_custom_dataset(path_misspellings, dataset_name, sym_spell):

    name_template_dict = dataset_name + "_template_dict.txt"
    name_word_list = dataset_name + "_word_list.txt"
    name_symspell_dict = dataset_name + "_symspell_dict.txt"
    name_phonenems_dict = dataset_name + "_phonemes_dict.txt"
    name_phonemes_sym = dataset_name + "_phonemes_sym.txt"

    template = dataset_processing.create_default_dict(path_misspellings)
    dataset_processing.pyspell_dict(template, dataset_name)
    dataset_processing.pickle_output(template, name_template_dict)
    dataset_processing.g2p_word_list(template, name_word_list)
    dataset_processing.g2p_phoneme_list(dataset_name)
    sym = dataset_processing.symspell_word_dict(dataset_name, sym_spell)
    dataset_processing.pickle_output(sym, name_symspell_dict)
    phonemes = dataset_processing.add_phonemes(template, dataset_name)
    dataset_processing.pickle_output(phonemes, name_phonenems_dict)
    phonemes_sym = dataset_processing.symspell_phonemes('TOP', dataset_name)
    dataset_processing.pickle_output(phonemes_sym, name_phonemes_sym)