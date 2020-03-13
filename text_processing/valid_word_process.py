import pickle
from pathlib import Path


def pickle_valid_words():
    """
    Function which takes the valid word list (list of words that are valid but that are not in the enchant dictionary)
    and creates a set which is serialised as a pickle file for use in processing the text item.
    :return: None
    """
    valid_words_set = set()
    data_folder = Path("C:/Users/robert/Documents/zeeko_nlp/spelling_mistakes/")
    valid_words_file_input = data_folder / 'valid_words.txt'
    valid_words_set_output = data_folder / 'valid_words_set.txt'

    with open(valid_words_file_input, 'r') as valid_words:
        lines = valid_words.read().splitlines()
        for word in lines:
            valid_words_set.add(word)

    with open(valid_words_set_output, 'wb') as output_file:
        pickle.dump(valid_words_set, output_file)


if __name__ == "__main__":
    pickle_valid_words()
