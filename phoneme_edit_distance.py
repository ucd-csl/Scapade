import pandas as pd
import numpy as np
from tabulate import tabulate


def phoneme_edit_distance(w1, w2):

    similarities = pd.read_csv('input_files/acoustic_similarity.csv', index_col=0)

    # cost of insertion/deletion
    idc = 0.5

    # compare two seqs of phon
    def compare(string1, string2):
        r = string1
        h = string2

        d = np.zeros((len(r) + 1) * (len(h) + 1), dtype=float)
        d = d.reshape((len(r) + 1, len(h) + 1))

        e = np.zeros((len(r) + 1) * (len(h) + 1), dtype=object)
        e = e.reshape((len(r) + 1, len(h) + 1))

        for i in range(len(r) + 1):
            for j in range(len(h) + 1):
                if i == 0:
                    if j == 0:
                        d[0][0] = 0
                        e[0][j] = (0, 0, 0)
                    else:
                        d[i][j] = d[i][j - 1] + idc
                        e[0][j] = (0, 0, 1)
                elif j == 0:
                    if i == 0:
                        e[i][0] = (0, 0, 0)
                    else:
                        d[i][j] = d[i - 1][j] + idc
                        e[i][0] = (1, 0, 0)

        for i in range(1, len(r) + 1):
            for j in range(1, len(h) + 1):
                if r[i - 1] == h[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                    e[i][j] = (0, 1, 0)
                else:
                    # some random extra stuff in here that doesn't get used - could clean up but works as is
                    sub = ((d[i - 1][j - 1] + (score(r[i - 1], h[j - 1]))),
                           (str(e[i - 1][j - 1]) + 'substitution ' + str(j - 1) + ', '))
                    dell = (d[i - 1][j] + idc, (str(e[i][j - 1]) + 'deletion ' + str(j - 1) + ' ,'))
                    if j >= len(h):
                        ins = (d[i][j - 1] + idc, (str(e[i - 1][j]) + 'insertion ' + str(j) + ' ,'))
                    else:
                        ins = (d[i][j - 1] + idc, (str(e[i - 1][j]) + 'insertion ' + str(j) + ' ,'))
                    d[i][j] = min(sub, ins, dell)[0]
                    e[i][j] = (dell[0] == d[i][j], sub[0] == d[i][j], ins[0] == d[i][j]) * 1
                    # d = table of actual scores
        # e = keeps track of operations
        return d, e

    # individual phonemes
    def score(l1, l2):
        return similarities[str(l1)][str(l2)]

    # naive_backtrace and align code taken from the internet - uses the backtrace to find
    # the optimum path and alignment
    # https://giov.dev/2016/01/minimum-edit-distance-in-python.html

    # looks to find the smallest edit distance backwards through the matrix
    def naive_backtrace(B_matrix):

        i, j = B_matrix.shape[0] - 1, B_matrix.shape[1] - 1
        backtrace_idxs = [(i, j)]
        while (i, j) != (0, 0):
            if B_matrix[i, j][1]:
                i, j = i - 1, j - 1
            elif B_matrix[i, j][0]:
                i, j = i - 1, j
            elif B_matrix[i, j][2]:
                i, j = i, j - 1
            backtrace_idxs.append((i, j))

        return backtrace_idxs

    # uses back trace to align phonemes
    # mapping the two diff strings
    def align(word_1, word_2, bt):

        aligned_word_1 = []
        aligned_word_2 = []
        operations = []

        backtrace = bt[::-1]  # make it a forward trace

        for k in range(len(backtrace) - 1):
            i_0, j_0 = backtrace[k]
            i_1, j_1 = backtrace[k + 1]

            w_1_letter = None
            w_2_letter = None
            op = None

            if i_1 > i_0 and j_1 > j_0:  # either substitution or no-op
                if word_1[i_0] == word_2[j_0]:  # no-op, same symbol
                    w_1_letter = word_1[i_0]
                    w_2_letter = word_2[j_0]
                    op = " "
                else:  # cost increased: substitution
                    w_1_letter = word_1[i_0]
                    w_2_letter = word_2[j_0]
                    op = "s"
            elif i_0 == i_1:  # insertion
                w_1_letter = " "
                w_2_letter = word_2[j_0]
                op = "i"
            else:  # j_0 == j_1,  deletion
                w_1_letter = word_1[i_0]
                w_2_letter = " "
                op = "d"

            aligned_word_1.append(w_1_letter)
            aligned_word_2.append(w_2_letter)
            operations.append(op)

        return aligned_word_1, aligned_word_2, operations

    # pretty print of alignment table
    def make_table(alignment):
        row1 = []
        row2 = []
        row3 = []
        for i, j, k in alignment:
            row1.append(i)
            row2.append(j)
            row3.append(k)
        table = [row1, row2, row3]
        return table

    def align_and_score(word1, word2):
        d, e = compare(word1, word2)
        bt = naive_backtrace(e)
        a, b, c = (align(word1, word2, bt))
        alignment = (list(zip(a, b, c)))
        x, y = d.shape
        score = (d[x - 1][y - 1])
        # table = make_table(alignment)
        # print(tabulate(table))

        return score

