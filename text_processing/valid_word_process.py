import pickle
from pathlib import Path


def pickle_valid_words():

    valid_words_set = set()
    data_folder = Path("C:/Users/robert/Documents/zeeko_nlp/spelling_mistakes/")
    valid_words_file = data_folder / 'valid_words.txt'

    with open(valid_words_file, 'r') as valid_words:
        for word in valid_words:
            valid_words_set.add(word)

    with open('valid_words_set.txt', 'wb') as output_file:
        pickle.dump(valid_words_set, output_file)


if __name__ == "__main__":
    pickle_valid_words()
