from text_processing import dataset_processing
from data_analysis import create_results_csv
from pathlib import Path
import os

print("Please enter the name of the dataset in /input_files/. Eg. 'custom.txt'")
user_dataset_name = input("Enter dataset name: ")
input_path_files = "../input_files/"
input_path_files = Path(input_path_files) / user_dataset_name
output_path_files = "../input_files/spelling_correction_dicts"


def check_make_dir(user_dataset_name):
    path_results = '../data_analysis/results'
    path_results_dataset = Path(path_results) / user_dataset_name.split('.')[0]

    if not os.path.isdir(path_results_dataset):
        os.mkdir(path_results_dataset)
        os.mkdir(Path(path_results_dataset) / 'symspell_cmu_phonemes')

    if not os.path.isdir(Path(path_results_dataset) / 'symspell_cmu_phonemes'):
        os.mkdir(Path(path_results_dataset) / 'symspell_cmu_phonemes')


def process_custom_dataset(path_misspellings, dataset_name, sym_spell):

    name_template_dict = dataset_name + "_template_dict.txt"
    name_word_list = dataset_name + "_word_list.txt"
    name_symspell_dict = dataset_name + "_symspell_dict.txt"
    name_phonenems_dict = dataset_name + "_phonemes_dict.txt"
    name_phonemes_sym = dataset_name + "_phonemes_sym.txt"

    template = dataset_processing.create_default_dict(path_misspellings)
    dataset_processing.pickle_output(template, name_template_dict)
    dataset_processing.g2p_word_list(template, name_word_list)
    dataset_processing.g2p_phoneme_list(dataset_name)
    sym = dataset_processing.symspell_word_dict(dataset_name, sym_spell)
    dataset_processing.pickle_output(sym, name_symspell_dict)
    phonemes = dataset_processing.add_phonemes(template, dataset_name)
    dataset_processing.pickle_output(phonemes, name_phonenems_dict)
    phonemes_sym = dataset_processing.symspell_phonemes('TOP', dataset_name)
    dataset_processing.pickle_output(phonemes_sym, name_phonemes_sym)


def populate_results(user_dataset_name):
    user_dataset_name = user_dataset_name.split('.')[0]
    complete_corrections_path = "../input_files/spelling_correction_dicts/"
    output_path = "../data_analysis/results/"
    complete_results = {}
    output_paths = {}
    dataset_names = [user_dataset_name]

    for dataset in dataset_names:
        complete_results[dataset] = complete_corrections_path + dataset + '_phonemes_sym.txt'
        output_paths[dataset] = output_path + dataset + "/symspell_cmu_phonemes/" + "all_cmu_corrections.csv"

    results = create_results_csv.load_results(complete_results[dataset_names[0]])
    results_updated = create_results_csv.update_results_dict(results)
    df = create_results_csv.create_df_output(results_updated)
    create_results_csv.save_to_csv(df, output_paths[dataset_names[0]])


def main():

    check_make_dir(user_dataset_name)
    process_custom_dataset(input_path_files, user_dataset_name.split('.')[0], dataset_processing.create_sym_object())
    populate_results(user_dataset_name)


if __name__ == "main":
    main()