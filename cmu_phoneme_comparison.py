import pickle
from phoneme_edit_distance import phoneme_edit_distance


# 1 - misspelling - word
mw_dict={'opend': 'opened', 'mabey': 'maybe', 'preffered': 'preferred', 'freindly': 'friendly', 'meat': 'meet',
         'anoeing': 'annoying', 'detaled': 'detailed', 'respound': 'respond', 'preased': 'pressed', 'to': 'too',
         'meny': 'many', 'vioce': 'voice', 'exiting': 'exciting', 'apeal': 'appeal', 'comfertable': 'confortable',
         'detale': 'detail'}

# 2 - misspelling - phonemes
mph_dict={'opend': 'OW P AH N D', 'mabey': 'M EY B IY', 'preffered': 'P R EH F ER D', 'freindly': 'F R AY N D L IY',
          'meat': 'M IY T', 'anoeing': 'AH N UW IH NG', 'detaled': 'D IH T EY L D', 'respound': 'R IY S P AW N D',
          'preased': 'P R IY S T', 'to': 'T UW','meny': 'M EH N IY', 'vioce': 'V AY AH S',
          'exiting': 'EH G Z AH T IH NG', 'apeal': 'EY P IY L', 'comfertable': 'K AH M F ER T AH B AH L',
          'detale': 'D IH T EY L'}


with open("C:/Users/robert/Documents/zeeko_nlp/input_files/phonemes_set.txt", 'rb') as cmu_phonemes:
    cmu_phonemes = pickle.load(cmu_phonemes)
    close_seq_of_phonemes_dict = {}

    # results_dict len = 34013
    for misspelling in list(mph_dict)[0:]:
        close_seq_of_phonemes = []

        # phonemes seq associated to the misspelling
        phonemes = mph_dict.get(misspelling)
        phonemes_list = phonemes.split(" ")

        # make sure the list of close phonemes also contains the misspelled word's phonemes
        # List of close sequence of phonemes?


        # for each phoneme string sequence for mispelled word, add to list close_seq_phonemes
        close_seq_of_phonemes.append(phonemes)

        # for each unique phoneme sequence in the cmu dict
        for i in cmu_phonemes:

            # split sequence into individual phonemes
            j = i.split(" ")

            if j[:1] == phonemes_list[:1]:
                if j[-1] == phonemes_list[-1]:
                    dist = phoneme_edit_distance(phonemes_list, j)  # Emma's distance for phonemes
                    try:
                        if dist <= 0.5:
                            close_seq_of_phonemes.append(i)
                    except:
                        print(j[-1])
                        print( phonemes_list[-1])
        close_seq_of_phonemes_dict[misspelling] = close_seq_of_phonemes