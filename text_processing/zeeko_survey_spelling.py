import enchant
import emoji
import pandas as pd
from pathlib import Path
from os import listdir
from os.path import isfile, join

d = enchant.Dict("en_GB")


def load_xlsx():

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
    processed_text = emoji.get_emoji_regexp().sub(u'', input_text)
    replace_rules = {".": " ", ",": " ", "’": "'", "\n": " ", '\r': " ",  "(": "", ")": ""}
    processed_text = (processed_text.translate(str.maketrans(replace_rules))).lower().split()
    return processed_text


def find_mistakes(processed_text):
    spelling_mistakes = set()
    for word in processed_text:
        if not d.check(word):
            spelling_mistakes.add(word)
    return spelling_mistakes


def save_output(mistakes_set):
    with open('xlsx_output.txt', 'w', encoding="utf-8") as output_file:
        for mistake in mistakes_set:
            if mistake not in custom_valid_words:
                output_file.write("%s\n" % mistake)


if __name__ == "__main__":
    all_df_dict = load_xlsx()
    text = extract_text(all_df_dict)
    cleaned_text = clean_text(text)
    mistakes = find_mistakes(cleaned_text)
    save_output(mistakes)
