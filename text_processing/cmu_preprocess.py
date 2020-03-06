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


with open("C:/Users/robert/Documents/zeeko_nlp/input_files/cmudict-0.7b", "r") as cmu_dict_file:

    cmu_dict = {}
    cmu_phones = []
    cmu_dict2 = {}

    # creating dictionary for cmu dict
    # create one dictionary with phones as key and word as values
    # create a second dictionary with word as key and phone as value
    for line in cmu_dict_file:

        line_processed = process_lines(line)

        # Make sure that we start by a letter from the alphabet, lower or upper case
        if line_processed and line_processed[0].isalpha():
            word, phonemes = line_processed.split("  ")


            cmu_dict2[word.lower()] = phonemes
            cmu_dict[phonemes] = word.lower()
            cmu_phones.append(phonemes)

    print(len(cmu_dict))
    print(len(cmu_dict2))

    dict_1 = open("dict1.txt", 'w')
    dict_1.write(str(cmu_dict))
    dict_1.close()
    dict_2 = open("dict2.txt", 'w')
    dict_2.write(str(cmu_dict2))
    dict_2.close()

