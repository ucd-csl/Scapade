import enchant
import emoji
import pandas as pd
from pathlib import Path

d = enchant.Dict("en_GB")

test_text = """That the character can do a cartwheel.
The floss😆
Sound when you click on the phone
Not really
If you get past a certain level then you can fly.
When you have finished it teleports you there.
You could add a Quiz to test how good we learnt of this game
Nothing because it is very good and perfect the way it is
Many a real life situation that they have to solve
A real interdent
Maybe some spot the wright answer and the not
You could do like you have to beat people in it like your friends   Or you could be getting chased by something and you have to get away from it or you go back to the start
You could make the character dance
No l do not
No only you could make it easier to use to places maybe a teleporter to teleport you to the next phone
Some interactive games to play but also for learning and maybe have a video to watch  every lesson about a problem and we have to help solve the problems
The worm or a robot dance
Side games
Flossing and moon walking 🚶‍♀️
The floss
The floss and the worm and electro shuffle
No because it is already fun
The floss, when you finish a level you have to choose one door out off three if you get the wrong one you have to try again
The floss
"""


def load_xlsx():
    data_folder = Path("C:/Users/robert/Documents/zeeko_nlp/zeeko_surveys/")
    file_to_open = data_folder / "APPYNESS POST EQUALS TRUST TRIAL 1 Burton Joyce A.xlsx"
    df_survey = pd.read_excel(file_to_open, header=1)
    return df_survey


def extract_text(df):

    all_text = ""
    for column in df.columns:
        if column[:4] == 'Open':
            for row in df[column]:
                if not pd.isnull(row):
                    all_text += row + " "
    return all_text


def clean_text(input_text):
    processed_text = emoji.get_emoji_regexp().sub(u'', input_text)
    # replace_rules = {".": " ", ",": " ", "’": "'", "\n": " ", '\r': " ",  "(": "", ")": ""}
    replace_rules = {".": " ", ",": " ", "’": "'", "\n": " ", '\r': " ",  "(": "", ")": ""}
    processed_text = (processed_text.translate(str.maketrans(replace_rules))).lower().split()
    return processed_text


def find_mistakes(processed_text):
    spelling_mistakes = set()
    for word in processed_text:
        if not d.check(word):
            spelling_mistakes.add(word)
    return spelling_mistakes


if __name__ == "__main__":
    df = load_xlsx()
    text = extract_text(df)
    cleaned_text = clean_text(text)
    mistakes = find_mistakes(cleaned_text)
    print(mistakes)
