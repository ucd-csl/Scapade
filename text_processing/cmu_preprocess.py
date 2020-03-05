from string import digits


def process_lines(input_line):

    input_line = input_line.strip()
    remove_digits = str.maketrans('', '', digits)
    input_line = input_line.translate(remove_digits)
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
            word = word.strip("()")




            # cmu_dict2[word.lower()] = phones
            # cmu_dict[phones] = word.lower()
            # cmu_phones.append(phones)



