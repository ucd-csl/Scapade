import re


def process_lines(input_line):
    """

    :param input_line:
    :return:
    """

    input_line = input_line.strip()
    pattern = re.compile(r'[0-9+()]')
    input_line = pattern.sub("", input_line)
    return input_line


def write_output(phoneme2word, phonemes_set):

    phoneme2word_out = open("phoneme2word_dict.txt", 'w')
    phoneme2word_out.write(str(phoneme2word))
    phoneme2word_out.close()

    phonemes_set_out = open("phonemes_set.txt", 'w')
    phonemes_set_out.write(str(phonemes_set))
    phonemes_set_out.close()


with open("C:/Users/robert/Documents/zeeko_nlp/input_files/cmudict-0.7b", "r") as cmu_dict_file:

    cmu_phoneme2word = {}
    cmu_phonemes_set = set()
    cmu_output = open('cmu_processed.csv', 'w')

    for line in cmu_dict_file:
        line_processed = process_lines(line)

        if line_processed and line_processed[0].isalpha():
            word, phonemes = line_processed.split("  ")
            word = word.lower()
            cmu_phonemes_set.add(phonemes)
            cmu_output.write(word + "," + phonemes + "\n")

            if phonemes in cmu_phoneme2word:
                cmu_phoneme2word[phonemes].append(word)
            else:
                cmu_phoneme2word[phonemes] = [word]
    cmu_output.close()
    write_output(cmu_phoneme2word, cmu_phonemes_set)
