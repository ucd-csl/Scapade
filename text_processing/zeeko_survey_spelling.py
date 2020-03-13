import enchant
import emoji
import pickle
import pandas as pd
from pathlib import Path
from os import listdir
from os.path import isfile, join

d = enchant.Dict("en_GB")


def load_xlsx():
    """
    Each Zeeko survey is stored in an xlsx file. This script navigates to the folder and loads each of these scripts,
    storing them in a dictionary. The second row is taken as the header as this row contains the key-word "Open-Ended"
    in the column titles.
    :return: A dictionary of dataframes of each loaded xlsx file.
    """
    data_folder = Path("C:/Users/robert/Documents/zeeko_nlp/zeeko_surveys/")
    all_xlsx_files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
    df_dict = {}
    k = 0
    for xlsx_file in all_xlsx_files:
        file_to_open = data_folder / xlsx_file
        df_survey = pd.read_excel(file_to_open, header=1)
        df_dict[k] = df_survey
        k += 1
    return df_dict


def extract_text(df_dict):
    """
    Opens each dataframe in the input dictionary and checks if any of the columns contain the keyword "Open". If so,
    it then checks if each row is a valid string (not a number/empty). If true, it adds the row string value to the
    string 'all_text'. This is carried out for all dataframes and columns.
    :param df_dict: a dictionary of loaded xlsx files in dataframe format.
    :return: a string containing all valid free text entries from all dataframes (all of the xlsx files)
    """
    all_text = ""
    for k, v in df_dict.items():
        for column in v.columns:
            try:
                if column[:4] == 'Open':
                    for row in v[column]:
                        if not pd.isnull(row) and type(row) == str:
                            all_text += row + " "
            except Exception as e:
                print(e)
    return all_text


def clean_text(input_text):
    """
    Takes the string containing all valid open-ended survey responses as input and processes the text in a number of
    ways. This involves stripping emojis, special/invalid characters and then splitting the text on white space to
    obtain each individual word in list format.
    :param input_text:
    :return: a list of individual words
    """
    processed_text = emoji.get_emoji_regexp().sub(u'', input_text)
    replace_rules = {".": " ", ",": " ", "’": "'", "“": "", "\n": " ", '\r': " ",  "(": "", ")": "", "!": "", "#": "",
                     "?": "", "&": "", "`": "'", ":": "", "/": "", ";": "", "[": "", "]": ""}
    processed_text = (processed_text.translate(str.maketrans(replace_rules))).split()
    return processed_text


def find_mistakes(processed_text):
    """
    Takes as input the list of pre-processed words from the open-ended survey responses. It checks each word in it's
    current form and as a lower case to see if it is in either the enchant en_GB dictionary. If not, it is identified
    as a spelling mistake and added to a set (to ensure no duplication of spelling mistakes.
    :param processed_text: a list of preprocessed words
    :return: a set of words identified as spelling mistakes.
    """
    spelling_mistakes = set()
    for word in processed_text:
        if not d.check(word) and not d.check(word.lower()):
            spelling_mistakes.add(word.lower())
    return spelling_mistakes


def save_output(mistakes_set):
    """
    Takes as input a set of mispelled words, as determined by the enchant module. Checks this against a user custom list
    to ensure they are invalid (for example enchant identifies app names, social media and video game names as invalid).
    Function writes each of this misspelled words, line by line to an output file.
    :param mistakes_set:
    :return: None
    """
    data_folder = Path("C:/Users/robert/Documents/zeeko_nlp/spelling_mistakes/")
    custom_valid_words_path = data_folder / 'valid_words_set.txt'
    pickle_in = open(custom_valid_words_path, "rb")
    custom_valid_words = pickle.load(pickle_in)
    spelling_mistakes_output = data_folder / 'zeeko_spelling_mistakes_list.txt'

    with open(spelling_mistakes_output, 'w', encoding="utf-8") as output_file:
        for mistake in mistakes_set:
            if mistake not in custom_valid_words:
                output_file.write("%s\n" % mistake)


if __name__ == "__main__":
    all_df_dict = load_xlsx()
    text = extract_text(all_df_dict)
    cleaned_text = clean_text(text)
    mistakes = find_mistakes(cleaned_text)
    save_output(mistakes)
