"""
.. module:: editdistance
   :synopsis: Module for edit distance algorithms.
"""
from enum import Enum

import numpy as np
import pandas as pd
from pathlib import Path


import symspellpy_phonemes.helpers as helpers

class DistanceAlgorithm(Enum):
    """Supported edit distance algorithms"""
    LEVENSHTEIN_PHONEME = 0
    # LEVENSHTEIN = 0  #: Levenshtein algorithm.
    # DAMERUAUOSA = 1  #: Damerau optimal string alignment algorithm


class EditDistance(object):
    """Edit distance algorithms.

    Parameters
    ----------
    algorithm : :class:`DistanceAlgorithm`
        The distance algorithm to use.

    Attributes
    ----------
    _algorithm : :class:`DistanceAlgorithm`
        The edit distance algorithm to use.
    _distance_comparer : :class:`AbstractDistanceComparer`
        An object to compute the relative distance between two strings.
        The concrete object will be chosen based on the value of
        :attr:`_algorithm`

    Raises
    ------
    ValueError
        If `algorithm` specifies an invalid distance algorithm.
    """
    def __init__(self, algorithm):
        self._algorithm = algorithm
        if algorithm == DistanceAlgorithm.LEVENSHTEIN_PHONEME:
            self._distance_comparer = Levenshtein_Phoneme()
        else:
            raise ValueError("Unknown distance algorithm")

    def compare(self, string_1, string_2, max_distance):
        """Compare a string to the base string to determine the edit
        distance, using the previously selected algorithm.

        Parameters
        ----------
        string_1 : str
            Base string.
        string_2 : str
            The string to compare.
        max_distance : int
            The maximum distance allowed.

        Returns
        -------
        int
            The edit distance (or -1 if `max_distance` exceeded).
        """
        return self._distance_comparer.distance(string_1, string_2,
                                                max_distance)

class AbstractDistanceComparer(object):
    """An interface to compute relative distance between two strings"""
    def distance(self, string_1, string_2, max_distance):
        """Return a measure of the distance between two strings.

        Parameters
        ----------
        string_1 : str
            One of the strings to compare.
        string_2 : str
            The other string to compare.
        max_distance : int
            The maximum distance that is of interest.

        Returns
        -------
        int
            -1 if the distance is greater than the max_distance, 0 if
            the strings are equivalent, otherwise a positive number
            whose magnitude increases as difference between the strings
            increases.

        Raises
        ------
        NotImplementedError
            If called from abstract class instead of concrete class
        """
        raise NotImplementedError("Should have implemented this")


class Levenshtein_Phoneme(AbstractDistanceComparer):
    """Class providing Levenshtein algorithm for computing edit
    distance metric between two strings

    Attributes
    ----------
    _base_char_1_costs : numpy.ndarray
    """
    def __init__(self):
        self._base_char_1_costs = np.zeros(0, dtype=np.int32)

    def distance(self, string_1, string_2, max_distance):
        """Compute and return the Levenshtein edit distance between two
        strings.

        Parameters
        ----------
        string_1 : str
            One of the strings to compare.
        string_2 : str
            The other string to compare.
        max_distance : int
            The maximum distance that is of interest.

        Returns
        -------
        int
            -1 if the distance is greater than the maxDistance, 0 if
            the strings are equivalent, otherwise a positive number
            whose magnitude increases as difference between the strings
            increases.
        """
        string_1 = string_1.split()
        string_2 = string_2.split()

        if string_1 is None or string_2 is None:
            return helpers.null_distance_results(string_1, string_2,
                                                 max_distance)
        if max_distance <= 0:
            return 0 if string_1 == string_2 else -1
        max_distance = max_distance = int(min(2 ** 31 - 1, max_distance))
        # if strings of different lengths, ensure shorter string is in
        # string_1. This can result in a little faster speed by
        # spending more time spinning just the inner loop during the
        # main processing.
        if len(string_1) > len(string_2):
            string_2, string_1 = string_1, string_2
        if len(string_2) - len(string_1) > max_distance:
            return -1
        # identify common suffix and/or prefix that can be ignored
        len_1, len_2, start = helpers.prefix_suffix_prep(string_1, string_2)
        if len_1 == 0:
            return len_2 if len_2 <= max_distance else -1
        if len_2 > len(self._base_char_1_costs):
            self._base_char_1_costs = np.zeros(len_2, dtype=np.int32)
        # if max_distance < len_2:
        #     return self._distance_max(string_1, string_2, len_1, len_2,
        #                               start, max_distance,
        #                               self._base_char_1_costs)

        return self._distance(string_1, string_2)

    def _distance(self, string_1, string_2):
        """Internal implementation of the core Levenshtein algorithm.

        **From**: https://github.com/softwx/SoftWx.Match
        """
        input_path_files = "../symspellpy_phonemes/"
        file_name = 'acoustic_distributional_distance_matrix.csv'
        input_file = Path(input_path_files) / file_name
        similarities = pd.read_csv(input_file, index_col=0)

        # cost of insertion/deletion
        idc = 1

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

        def align_and_score(word1, word2):
            d, e = compare(word1, word2)
            bt = naive_backtrace(e)
            a, b, c = (align(word1, word2, bt))
            x, y = d.shape
            score = (d[x - 1][y - 1])
            return score
        return align_and_score(string_1, string_2)
    #
    # def _distance_max(self, string_1, string_2, len_1, len_2, start,
    #                   max_distance, char_1_costs):
    #     """Internal implementation of the core Levenshtein algorithm
    #     that accepts a max_distance.
    #
    #     **From**: https://github.com/softwx/SoftWx.Match
    #     """
    #     char_1_costs = np.asarray([j + 1 if j < max_distance
    #                                else max_distance + 1
    #                                for j in range(len_2)])
    #     len_diff = len_2 - len_1
    #     j_start_offset = max_distance - len_diff
    #     j_start = 0
    #     j_end = max_distance
    #     current_cost = 0
    #     for i in range(len_1):
    #         char_1 = string_1[start + i]
    #         prev_char_1_cost = above_char_cost = i
    #         # no need to look beyond window of lower right
    #         # diagonal - max_distance cells (lower right diag is
    #         # i - lenDiff) and the upper left diagonal +
    #         # max_distance cells (upper left is i)
    #         j_start += 1 if i > j_start_offset else 0
    #         j_end += 1 if j_end < len_2 else 0
    #         for j in range(j_start, j_end):
    #             # cost of diagonal (substitution)
    #             current_cost = prev_char_1_cost
    #             prev_char_1_cost = char_1_costs[j]
    #             if string_2[start + j] != char_1:
    #                 # substitution if neither of the two conditions
    #                 # below
    #                 if above_char_cost < current_cost:
    #                     current_cost = above_char_cost
    #                 if prev_char_1_cost < current_cost:
    #                     current_cost = prev_char_1_cost
    #                 current_cost += 0.5
    #             char_1_costs[j] = above_char_cost = current_cost
    #         if char_1_costs[i + len_diff] > max_distance:
    #             return -1
    #     return current_cost if current_cost <= max_distance else -1
    # def _distance_max(self, string_1, string_2, len_1, len_2, start,
    #                   max_distance, char_1_costs):
    #     """Internal implementation of the core Levenshtein algorithm
    #     that accepts a max_distance.
    #
    #     **From**: https://github.com/softwx/SoftWx.Match
    #     """
    #     char_1_costs = np.asarray([j + 1 if j < max_distance
    #                                else max_distance + 1
    #                                for j in range(len_2)])
    #     len_diff = len_2 - len_1
    #     j_start_offset = max_distance - len_diff
    #     j_start = 0
    #     j_end = max_distance
    #     current_cost = 0
    #     for i in range(len_1):
    #         char_1 = string_1[start + i]
    #         prev_char_1_cost = above_char_cost = i
    #         # no need to look beyond window of lower right
    #         # diagonal - max_distance cells (lower right diag is
    #         # i - lenDiff) and the upper left diagonal +
    #         # max_distance cells (upper left is i)
    #         j_start += 1 if i > j_start_offset else 0
    #         j_end += 1 if j_end < len_2 else 0
    #         for j in range(j_start, j_end):
    #             # cost of diagonal (substitution)
    #             current_cost = prev_char_1_cost
    #             prev_char_1_cost = char_1_costs[j]
    #             if string_2[start + j] != char_1:
    #                 # substitution if neither of the two conditions
    #                 # below
    #                 if above_char_cost < current_cost:
    #                     current_cost = above_char_cost
    #                 if prev_char_1_cost < current_cost:
    #                     current_cost = prev_char_1_cost
    #                 current_cost += 0.5
    #             char_1_costs[j] = above_char_cost = current_cost
    #         if char_1_costs[i + len_diff] > max_distance:
    #             return -1
    #     return current_cost if current_cost <= max_distance else -1

