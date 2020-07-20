from pathlib import Path
import pandas as pd
import pickle

def overlap(dict_1, dict_2, dict_1_name, dict_2_name, data_name, comparison_name):
    """
    Calculates the 'overlap' between the results of two spelling correction methods on the same dataset

    :param dict_1: first spelling correction python dictionary object to compare.
    :param dict_2: second spelling correction python dictionary object to compare.
    :param dict_1_name: name of the first python dictionary object eg. 'pyspell'.
    :param dict_2_name: name of the second python dictionary object eg. 'scapade'.
    :param data_name: dataset used eg. 'holbrook'. Used for outputting results to correct directory. \
        Currently used names = ['aspell', 'birkbeck', 'holbrook', 'wiki', 'zeeko']
    :param comparison_name: the comparison of the two methods used eg. 'pyspell_scapade'. Used to output \
        to the correct sub-dir. Currently used = ['pyspell_scapade', 'symspell_scapade']
    :output: Writes the results to the respect directories and sub-directories.
    :return: Returns the values for unique corrections per method, and the overlap between the two.

    Example: overlap(holbrook_pyspell, holbrook_phonemes, 'pyspell', 'scapade', 'holbrook', \
    'pyspell_scapade')
    """
    path = "results/" + data_name + "/" + comparison_name + "/"
    Path(path).mkdir(parents=True, exist_ok=True)

    both_correct_count = 0
    dict_1_correct_count = 0
    dict_2_correct_count = 0

    both_correct_list = []
    dict_1_correct_list = []
    dict_2_correct_list = []

    for key in dict_1.keys():

        if dict_1[key]['suggested'] == dict_2[key]['suggested']:
            if dict_1[key]['suggested'] == dict_1[key]['correct_spelling']:
                both_correct_count += 1
                misspelling = key
                suggestion = dict_1[key]['correct_spelling']
                both_correct_list.append({'Misspelling': misspelling,
                                          'Suggestion': suggestion})

        elif dict_1[key]['suggested'] == dict_1[key]['correct_spelling']:
            dict_1_correct_count += 1
            misspelling = key
            suggestion = dict_1[key]['correct_spelling']
            dict_1_correct_list.append({'Misspelling': misspelling,
                                        'suggestion': suggestion})

        elif dict_2[key]['suggested'] == dict_2[key]['correct_spelling']:
            dict_2_correct_count += 1
            misspelling = key
            suggestion = dict_2[key]['correct_spelling']
            dict_2_correct_list.append({'Misspelling': misspelling,
                                        'Suggestion': suggestion})

    df_both = pd.DataFrame(both_correct_list)
    df_dict_1 = pd.DataFrame(dict_1_correct_list)
    df_dict_2 = pd.DataFrame(dict_2_correct_list)

    df_both.to_csv((path + 'both.csv'), index=False)
    df_dict_1.to_csv((path + dict_1_name + '.csv'), index=False)
    df_dict_2.to_csv((path + dict_2_name + '.csv'), index=False)

    return ({'both': both_correct_count, dict_1_name: dict_1_correct_count,
             dict_2_name: dict_2_correct_count})


def overlap_cand(dict_1, dict_2, dict_1_name, dict_2_name, data_name, comparison_name):
    """
    Calculates the 'overlap' between the results of two spelling correction methods on the same dataset

    :param dict_1: first spelling correction python dictionary object to compare.
    :param dict_2: second spelling correction python dictionary object to compare.
    :param dict_1_name: name of the first python dictionary object eg. 'pyspell'.
    :param dict_2_name: name of the second python dictionary object eg. 'scapade'.
    :param data_name: dataset used eg. 'holbrook'. Used for outputting results to correct directory. \
        Currently used names = ['aspell', 'birkbeck', 'holbrook', 'wiki', 'zeeko']
    :param comparison_name: the comparison of the two methods used eg. 'pyspell_scapade'. Used to output \
        to the correct sub-dir. Currently used = ['pyspell_scapade', 'symspell_scapade']
    :output: Writes the results to the respect directories and sub-directories.
    :return: Returns the values for unique corrections per method, and the overlap between the two.

    Example: overlap(holbrook_pyspell, holbrook_phonemes, 'pyspell', 'scapade', 'holbrook', \
    'pyspell_scapade')
    """
    path = "results/" + data_name + "/" + comparison_name + "/"

    both_correct_count = 0
    dict_1_correct_count = 0
    dict_2_correct_count = 0

    both_correct_list = []
    dict_1_correct_list = []
    dict_2_correct_list = []

    for key in dict_1.keys():

        target = dict_1[key]['correct_spelling']

        if target in dict_1[key]['candidates'] and target in dict_2[key]['candidates']:
            both_correct_count += 1
            misspelling = key
            suggestion = dict_1[key]['correct_spelling']
            both_correct_list.append({'Misspelling': misspelling,
                                      'Suggestion': suggestion})

        elif target in dict_1[key]['candidates']:
            dict_1_correct_count += 1
            misspelling = key
            suggestion = dict_1[key]['correct_spelling']
            dict_1_correct_list.append({'Misspelling': misspelling,
                                        'suggestion': suggestion})

        elif target in dict_2[key]['candidates']:
            dict_2_correct_count += 1
            misspelling = key
            suggestion = dict_2[key]['correct_spelling']
            dict_2_correct_list.append({'Misspelling': misspelling,
                                        'Suggestion': suggestion})

    df_both = pd.DataFrame(both_correct_list)
    df_dict_1 = pd.DataFrame(dict_1_correct_list)
    df_dict_2 = pd.DataFrame(dict_2_correct_list)

    df_both.to_csv((path + 'both.csv'), index=False)
    df_dict_1.to_csv((path + dict_1_name + '.csv'), index=False)
    df_dict_2.to_csv((path + dict_2_name + '.csv'), index=False)

    return ({'both': both_correct_count, dict_1_name: dict_1_correct_count,
             dict_2_name: dict_2_correct_count})


def score_application(name, input_dict):
    """
    Calculates and returns the scores for a given method and results dictionary
    :param name: the name of the method as a string eg. 'SymSpell'
    :param input_dict: the input dict of spelling corrections to be score eg.
    'holbrook_symspell'
    :returns: a dictionary of results
    """
    correct = 0
    candidates = 0
    for misspelling, results in input_dict.items():
        try:
            if results['correct_spelling'] == results['suggested']:
                correct += 1
            elif results['correct_spelling'] in results['candidates']:
                candidates += 1
        except:
            results['suggested'] = ''
            results['candidates'] = ''

    correct_and_candidates = correct + candidates

    results = {'Spelling Application': name, 'Correct': correct,
               'Candidates': candidates,
               'Correct_and_Candidates': correct_and_candidates}

    return results


def assign_scores(df, name):
    """Function to assign scores for each dataset and method"""

    dict = {}

    dict[name + '_pyspell_acc'] = int(df[df['Spelling Application'] == 'PySpell']['Correct'])
    dict[name + '_symspell_acc'] = int(df[df['Spelling Application'] == 'SymSpell']['Correct'])
    dict[name + '_aspell_acc'] = int(df[df['Spelling Application'] == 'Aspell']['Correct'])
    dict[name + '_phoneme_acc'] = int(df[df['Spelling Application'] == 'S-capade']['Correct'])

    dict[name + '_pyspell_cand'] = int(df[df['Spelling Application'] == 'PySpell']['Candidates'])
    dict[name + '_symspell_cand'] = int(df[df['Spelling Application'] == 'SymSpell']['Candidates'])
    dict[name + '_aspell_cand'] = int(df[df['Spelling Application'] == 'Aspell']['Candidates'])
    dict[name + '_phoneme_cand'] = int(df[df['Spelling Application'] == 'S-capade']['Candidates'])

    dict[name + '_pyspell_comb'] = int(df[df['Spelling Application'] == 'PySpell']['Correct_and_Candidates'])
    dict[name + '_symspell_comb'] = int(df[df['Spelling Application'] == 'SymSpell']['Correct_and_Candidates'])
    dict[name + '_aspell_comb'] = int(df[df['Spelling Application'] == 'Aspell']['Correct_and_Candidates'])
    dict[name + '_phoneme_comb'] = int(df[df['Spelling Application'] == 'S-capade']['Correct_and_Candidates'])

    return dict


def print_scores(dic, name, total_words):
    """Function to print scores for each dataset and method"""

    print("PySpell Accuracy:", str(round(dic[name + '_pyspell_acc'] / total_words * 100, 2)) + "%")
    print("SymSpell Accuracy:", str(round(dic[name + '_symspell_acc'] / total_words * 100, 2)) + "%")
    print("Aspell Accuracy:", str(round(dic[name + '_aspell_acc'] / total_words * 100, 2)) + "%")
    print("Phoneme Accuracy:", str(round(dic[name + '_phoneme_acc'] / total_words * 100, 2)) + "%\n")

    print("PySpell Correct Answer in Candidates List:",
          str(round(dic[name + '_pyspell_cand'] / total_words * 100, 2)) + "%")
    print("SymSpell Correct Answer in Candidates List:",
          str(round(dic[name + '_symspell_cand'] / total_words * 100, 2)) + "%")
    print("Aspell Correct Answer in Candidates List:",
          str(round(dic[name + '_aspell_cand'] / total_words * 100, 2)) + "%")
    print("Phoneme Correct Answer in Candidates List:",
          str(round(dic[name + '_phoneme_cand'] / total_words * 100, 2)) + "%\n")

    print("PySpell Recall (Correct + Correct in Candidates List):",
          str(round(dic[name + '_pyspell_comb'] / total_words * 100, 2)) + "%")
    print("SymSpell Recall (Correct + Correct in Candidates List):",
          str(round(dic[name + '_symspell_comb'] / total_words * 100, 2)) + "%")
    print("Aspell Recall (Correct + Correct in Candidates List):",
          str(round(dic[name + '_aspell_comb'] / total_words * 100, 2)) + "%")
    print("Phoneme Recall (Correct + Correct in Candidates List):",
          str(round(dic[name + '_phoneme_comb'] / total_words * 100, 2)) + "%")


def print_overlap_scores(dict, compare_to):
    """Prints the overlap scores for a given input dict of results"""

    compare_to_low = compare_to.lower()
    total_corrections = dict['both'] + dict[compare_to_low] + dict['scapade']
    print("Total corrections:", total_corrections)
    print("Overlap corrections: " + "{:.2f}".format(dict['both'] / total_corrections * 100) + "%")
    print("Unique corrections " + compare_to + ": " + "{:.2f}".format(
        dict[compare_to_low] / total_corrections * 100) + "%")
    print("Unique corrections S-capade method: " + "{:.2f}".format(dict['scapade'] /
                                                                  total_corrections * 100) + "%")


def scapade_all_attempts():
    """
    Function which generates the "scapade_all_attempts.csv" file for human review and reading. Run at the end of
    populating each of the results folders for all of the datasets. Currently does not have any error handling,
    only used for research and data review.
    :return:
    """

    complete_corrections_path = "../input_files/spelling_correction_dicts/"
    output_path = "../data_analysis/results/"
    dataset_names = ['holbrook', 'birkbeck', 'zeeko', 'aspell', 'wiki']
    complete_results = {}
    output_paths = {}

    for dataset in dataset_names:
        complete_results[dataset] = complete_corrections_path + dataset + '_phonemes_sym.txt'
        output_paths[dataset] = output_path + dataset + "/scapade_all_attempts.csv"

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

            # add statement to account for correct or in candidates

        return input_dict

    def create_df_output(input_dict):
        output = pd.DataFrame()
        for key, values in input_dict.items():
            output = output.append(input_dict[key], ignore_index=True)
        return output

    def save_to_csv(df, save_path):
        df.to_csv(save_path, index=False)

    def run():
        for dataset in dataset_names:
            results = load_results(complete_results[dataset])
            results_updated = update_results_dict(results)
            df = create_df_output(results_updated)
            df = df[['correct', 'in_candidates', 'correct_spelling', 'misspelling', 'phoneme_rep',
                     'suggested', 'suggested_phoneme', 'candidates']]
            save_to_csv(df, output_paths[dataset])

    run()
