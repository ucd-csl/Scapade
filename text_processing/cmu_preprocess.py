import re
import pickle
from pathlib import Path
import pandas as pd

path_files = "C:/Users/robert/Documents/zeeko_nlp/input_files/"


def valid_phonemes():
    """
    Loads to acoustic similarity matrix and extracts each Arpabet phoneme. Serialised as a pickle
    csv file for loading in other scripts.
    :return: None
    """
    similarities = Path(path_files) / 'acoustic_similarity.csv'
    similarities = pd.read_csv(similarities, index_col=0)
    phonemes = []
    for column in similarities.columns:
        phonemes.append(column)
    with open(path_files + "arpabet.csv", 'wb') as fp:
        pickle.dump(phonemes, fp)


def process_lines(input_line):
    """
    Takes the current line being read from the cmu dictionary, and processes according to the following rules:
    - Removes leading and trailing whitespace
    - Removes all digits
    - Removes parenthesis '()'

    :param input_line:
    :return: processed input line
    """
    input_line = input_line.strip()
    pattern = re.compile(r'[0-9+()]')
    input_line = pattern.sub("", input_line)
    return input_line


def write_output_phonemes(phoneme2word, phonemes_set):
    """
    Takes the dictionary of phonemes:words and the set of phonemes and writes them to pickle output files.

    :param phoneme2word:
    :param phonemes_set:
    :return: None
    """
    phonemes_set = sorted(phonemes_set)

    with open(path_files + "phoneme2word_dict.txt", 'wb') as fp:
        pickle.dump(phoneme2word, fp)

    with open(path_files + "phonemes_set.txt", 'wb') as fp:
        pickle.dump(phonemes_set, fp)


def write_output_freq_dict(frequency_dict):
    """
    Writes the processed frequency dictionary to text file named 'frequency_dict.txt

    :param frequency_dict:
    :return: None
    """
    freq_dict_out = open(path_files + "frequency_dict.txt", 'w')
    freq_dict_out.write(str(frequency_dict))
    freq_dict_out.close()


def cmu_dict_processing():
    """
    Carries out the main processing of the cmu dictionary into the desired formats. Also writes and updated version of
    the cmu dictionary to a csv, in the form word, phoneme.

    :return: None
    """
    with open(path_files + "cmudict-0.7b", 'r') as cmu_dict_file:

        cmu_phoneme2word = {}
        cmu_phonemes_set = set()
        cmu_output = open(path_files + "cmu_processed.csv", 'w')

        for line in cmu_dict_file:
            line_processed = process_lines(line)

            if line_processed and line_processed[0].isalpha():
                word, phonemes = line_processed.split("  ")
                word = word.lower()
                cmu_phonemes_set.add(phonemes)
                cmu_output.write(word + ',' + phonemes + "\n")

                if phonemes in cmu_phoneme2word:
                    cmu_phoneme2word[phonemes].append(word)
                else:
                    cmu_phoneme2word[phonemes] = [word]
        cmu_output.close()
        write_output_phonemes(cmu_phoneme2word, cmu_phonemes_set)


def frequency_dict_process():
    """
    Takes the frequency dictionary text file from SymSpell (https://github.com/wolfgarbe/SymSpell) and converts it
    into a Python dictionary and saves to file. Current dictionary used is: frequency_dictionary_en_82_765.txt
    :return:
    """
    frequency_dictionary = {}
    with open(path_files + "frequency_dictionary_en_82_765.txt") as frequency_dict_file:
        for line in frequency_dict_file:
            word, frequency = line.split()
            frequency_dictionary[word] = frequency
    write_output_freq_dict(frequency_dictionary)


def cmu_frequency_dict():
    cmu_dict = pd.read_csv(path_files + "cmu_processed.csv", names=['Word', 'Sequence', 'Frequency'], encoding = "ISO-8859-1")
    cmu_dict['Frequency'] = 1
    cmu_frequency_rows = []
    with open(path_files + "frequency_dict.txt") as frequency_dict:
        frequency_dict = eval(frequency_dict.read())
        for index, row in cmu_dict.iterrows():
            if row['Word'] in frequency_dict:
                row['Frequency'] = frequency_dict[row['Word']]
                cmu_frequency_rows.append(row)
            else:
                cmu_frequency_rows.append(row)

        cmu_frequency = pd.DataFrame(cmu_frequency_rows)
        cmu_frequency.to_csv(path_files + "cmu_frequency.csv", header=False, index=False)


if __name__ == "__main__":
    valid_phonemes()
    cmu_dict_processing()
    frequency_dict_process()
    cmu_frequency_dict()
