import re


path_files = "C:/Users/robert/Documents/zeeko_nlp/input_files/"


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
    Takes the dictionary of phonemes:words and the set of phonemes and writes them to output files.

    :param phoneme2word:
    :param phonemes_set:
    :return: None
    """
    phoneme2word_out = open(path_files + "phoneme2word_dict.txt", 'w')
    phoneme2word_out.write(str(phoneme2word))
    phoneme2word_out.close()

    phonemes_set_out = open(path_files + "phonemes_set.txt", 'w')
    phonemes_set_out.write(str(phonemes_set))
    phonemes_set_out.close()


def write_output_freq_dict(frequency_dict):
    """
    Takes the frequency dictionary text file from SymSpell (https://github.com/wolfgarbe/SymSpell) and converts it
    into a Python dictionary and saves to file. Current dictionary used is: frequency_dictionary_en_82_765.txt

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
    frequency_dictionary = {}
    with open(path_files + "frequency_dictionary_en_82_765.txt") as frequency_dict_file:
        for line in frequency_dict_file:
            word, frequency = line.split()
            frequency_dictionary[word] = frequency
    write_output_freq_dict(frequency_dictionary)


if __name__ == "__main__":
    cmu_dict_processing()
    frequency_dict_process()
