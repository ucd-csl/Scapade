
from string import digits

cmu_dict = {}
cmu_dict_file = open("C:/Users/robert/Documents/zeeko_nlp/input_files/cmudict-0.7b", "r")
cmu_phones = []
cmu_dict2 = {}

# creating dictionary for cmu dict
# create one dictionary with phones as key and word as values
# create a second dictionary with word as key and phone as value
for line in cmu_dict_file:
    line = line.strip()
    remove_digits = str.maketrans('', '', digits)
    line = line.translate(remove_digits)
    start = line[:1]
    # Make sure that we start by a letter from the alphabet, lower or upper case
    # ord("a") = 97 ||  ord("A") = 65 || ord("z") = 122 || ord(Z) = 90
    if (ord(start) > 64 and ord(start) < 91) or (ord(start) > 64 and ord(start) < 123):
        word, phones = line.split("  ")
        word = word.strip("()")
        cmu_dict2[word.lower()] = phones
        cmu_dict[phones] = word.lower()
        cmu_phones.append(phones)

print(len(cmu_dict))