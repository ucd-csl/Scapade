import pandas as pd
import pickle

complete_corrections_path = "../input_files/spelling_correction_dicts/"
output_path = "../data_analysis/results/"
dataset_names = ['holbrook', 'birkbeck', 'zeeko', 'aspell', 'wiki']
complete_results = {}
output_paths = {}

for dataset in dataset_names:
    complete_results[dataset] = complete_corrections_path + dataset + '_phonemes_sym.txt'
    output_paths[dataset] = output_path + dataset + "/symspell_cmu_phonemes/" + "all_cmu_corrections.csv"


def load_results(file_path):
    results = pickle.load(open(file_path, "rb"))
    return results


def update_results_dict(input_dict):
    for key in list(input_dict):
        input_dict[key]['misspelling'] = key
        if input_dict[key]['correct_spelling'] == input_dict[key]['suggested']:
            input_dict[key]['correct'] = 1
        else:
            input_dict[key]['correct'] = 0

        if input_dict[key]['correct_spelling'] in input_dict[key]['candidates']:
            input_dict[key]['in_candidates'] = 1
        else:
            input_dict[key]['in_candidates'] = 0

    return input_dict


def create_df_output(input_dict):
    output = pd.DataFrame()
    for key, values in input_dict.items():
        output = output.append(input_dict[key], ignore_index=True)
    return output


def save_to_csv(df, save_path):
    df.to_csv(save_path, index=False)


def main():

    for dataset in dataset_names:
        results = load_results(complete_results[dataset])
        results_updated = update_results_dict(results)
        df = create_df_output(results_updated)
        df = df[['correct', 'in_candidates', 'correct_spelling', 'misspelling', 'phoneme_rep',
                'suggested', 'suggested_phoneme', 'candidates']]
        save_to_csv(df, output_paths[dataset])


if __name__ == "__main__":
    main()