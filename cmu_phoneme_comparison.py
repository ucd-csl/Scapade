from phoneme_edit_distance import phoneme_edit_distance
import pandas as pd
from pathlib import Path
import timeit
import re

data_folder = Path("C:/Users/robert/Documents/zeeko_nlp/input_files/")
similarities = data_folder / 'acoustic_distributional_distance_matrix.csv'
similarities = pd.read_csv(similarities, index_col=0)

cmu_phonemes = data_folder / 'cmu_processed.csv'
cmu_phonemes = pd.read_csv(cmu_phonemes, encoding = "ISO-8859-1")


def arpabet_phonemes():
    arpa_phonemes = []
    for column in similarities.columns:
        arpa_phonemes.append(column)
    cmu_valid_phonemes = (cmu_phonemes.iloc[:, 1])
    cmu_valid_phonemes = cmu_valid_phonemes.tolist()

    return arpa_phonemes, cmu_valid_phonemes


#  https://norvig.com/spell-correct.html

def generate_phoneme_candidates(word, phonemes, valid_phonemes):

    def candidates(word):
        "Generate possible spelling corrections for word."
        return known(edits1(word)) or known(edits2(word))

    def known(words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in valid_phonemes)

    def edits1(word):
        "All edits that are one edit away from `word`."
        letters = phonemes
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [re.sub(' +', ' ',(L + " " + R[1:]).strip()) for L, R in splits if R]
        transposes = [re.sub(' +', ' ',(L + " " + R[1] + " " + R[0] + " " + R[2:]).strip()) for L, R in splits if len(R)>1]
        replaces = [re.sub(' +', ' ',(L + " " + c + " " + R[1:]).strip()) for L, R in splits if R for c in letters]
        inserts = [re.sub(' +', ' ',(L + " " + c + " " + R).replace("  ", " ").strip()) for L, R in splits for c in letters]
        return set([word] + deletes + transposes + replaces + inserts)

    def edits2(word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in edits1(word) for e2 in edits1(e1))

    return candidates(word)



start = timeit.default_timer()
phonemes, valid_phonemes = arpabet_phonemes()
word_candidates = (generate_phoneme_candidates('N OW N', phonemes, valid_phonemes))
scores = {}

for word in word_candidates:
    score_dist = phoneme_edit_distance('N OW N', word)
    if score_dist < 0.5:
        scores[word] = score_dist
min = 100
best = ""

for k,v in scores.items():
    if v < min:
        best = k
        min = v
print(best, min)


stop = timeit.default_timer()
print(scores)
print('Time: ', stop - start)
