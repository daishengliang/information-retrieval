# -*- coding: utf-8 -*-
"""Assignment #2: Basic Concepts in Information Theory.

This module use mutual Information to calculate the relateness of wordpair.

Created on Sat Sep 10 03:23:00 2016

@author: ShengliangDai

"""

from collections import Counter
import itertools
import math
import pandas as pd

# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name


def load_dataset(filename):
    data = pd.read_table(filename, header=None)
    return data


def all_pairs(V):
    """Make all unique pairs (order doesn't matter)

    Args:
        V: Vocabulary set of documents.

    Return:
        pairs: all word-word pairs in V.

    """
    pairs = itertools.combinations(V, 2)
    return pairs


def main():
    documents = load_dataset('cacm.trec.filtered.txt')
    V = []
    for d in documents.values:
        words = str(d[0]).split()
        for i in words:
            if i not in V:
                V.append(i)

    Vindex = convertToIndex(V)
    Vid = {v: k for k, v in Vindex.items()}

    D = []
    for d in documents.values:
        words = str(d[0]).split()
        row = []
        for i in words:
            row.append(Vindex[i])
        D.append(list(set(row)))

    for i in range(len(V)):
        V[i] = Vindex[V[i]]

    wordpair = all_pairs(V)
    occur = occurrence(D)
    single_occur = word_occur(D)
    MI = cal_MI(D, occur, wordpair, single_occur)
    most_common_10 = MI.most_common(10)
    for i in most_common_10:
        print(Vid[i[0][0]], Vid[i[0][1]], i[1])

    programming = Vindex['programming']

    res = Counter()
    for i in MI:
        if i[0] == programming or i[1] == programming:
            res[(Vid[i[0]], Vid[i[1]])] += MI[i]
    for i in res.most_common(5):
        print(i)


def word_occur(D):
    """Calculate occurrence of single word.

    Args:
        D: Documents.

    Return:
        cnt: Document Frequency Counter for all words.

    """
    cnt = Counter()
    for i in D:
        for j in i:
            cnt[j] += 1
    return cnt


def MIW(p_a1b1, p_a0b1, p_a1b0, p_a0b0, p_a1, p_b1, p_a0, p_b0):
    """Help function to compute mutual information.

    Args:
        p_a1b1: The probability of a=1, b=1.
        p_a0b1: The probability of a=0, b=1.
        p_a1b0: The probability of a=1, b=0.
        p_a0b0: The probability of a=0, b=0.
        p_a1: The probability of a=1.
        p_b1: The probability of b=1.
        p_a0: The probability of a=0.
        p_b0: The probability of b=0.

    Returns:
        Mutual information.

    """
    a = p_a1b1 * math.log2(p_a1b1 / (p_a1 * p_b1))
    b = p_a1b0 * math.log2(p_a1b0 / (p_a1 * p_b0))
    c = p_a0b1 * math.log2(p_a0b1 / (p_a0 * p_b1))
    d = p_a0b0 * math.log2(p_a0b0 / (p_a0 * p_b0))
    return a + b + c + d


def cal_MI(D, occur, wordpair, single_occur):
    """Calculate Mutual Information.

    Args:
        D: Documents.

        occur: Counter for all word pairs.

        wordpair: all word-word pairs in V.

        single_occur: Document Frequency Counter for all words.

    Return:
        MI: Mutual Information score for all word pairs.

    """
    MI = Counter()
    for i in wordpair:
        a = i[0]
        b = i[1]

        a1b1 = occur[i]
        a1b0 = single_occur[a] - a1b1
        a0b1 = single_occur[b] - a1b1
        a0b0 = len(D) - (single_occur[a] + single_occur[b] - a1b1)
        if a1b1 == 0 or a1b0 == 0 or a0b1 == 0 or a0b0 == 0:
            p_a1b1 = (a1b1 + 0.25) / (len(D) + 1)
            p_a1b0 = (a1b0 + 0.25) / (len(D) + 1)
            p_a0b1 = (a0b1 + 0.25) / (len(D) + 1)
            p_a0b0 = (a0b0 + 0.25) / (len(D) + 1)
        else:
            p_a1b1 = a1b1 / len(D)
            p_a1b0 = a1b0 / len(D)
            p_a0b1 = a0b1 / len(D)
            p_a0b0 = a0b0 / len(D)
        p_a1 = p_a1b1 + p_a1b0
        p_a0 = p_a0b1 + p_a0b0
        p_b1 = p_a1b1 + p_a0b1
        p_b0 = p_a1b0 + p_a0b0

        MI[i] += MIW(p_a1b1, p_a0b1, p_a1b0, p_a0b0, p_a1, p_b1, p_a0, p_b0)

    return MI


def occurrence(D):
    """Word-word co-occurrence in documents.

    Args:
        D: Documents.

    Return:
        cnt: Counter for all word pairs.

    """
    cnt = Counter()
    for item in D:
        pair_set = itertools.combinations(item, 2)
        for j in pair_set:
            pair = tuple(sorted(list(j)))
            cnt[pair] += 1
    return cnt


def convertToIndex(names):
    """Convert strings to indices.

    Args:
        names: A list of strings.

    Returns:
        A dictionary mapping strings to indices.

    """
    index = 0
    dic = {}
    for name in names:
        dic[name] = index
        index += 1
    return dic


if __name__ == '__main__':
    main()
