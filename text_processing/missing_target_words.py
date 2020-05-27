import pickle

# load in misspelling datasets
file_path = '../input_files/'
aspell = file_path + 'aspell.txt'
birkbeck = file_path + 'birkbeck.txt'
holbrook = file_path + 'holbrook-missp.txt'
wikipedia = file_path + 'wikipedia.txt'
zeeko = file_path + 'zeeko_misspellings.txt'

datasets = {'aspell': aspell, 'birkbeck': birkbeck, 'holbrook': holbrook, 'wikipedia': wikipedia, 'zeeko': zeeko}

# get all the target misspellings for each dataset and store these as lower case words in a set
all_set = set()

for key, value in datasets.items():
    with open(datasets[key], 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            if line[0] == '$' and '_' not in line:
                all_set.add(line[1:].lower())

print(len(all_set))
