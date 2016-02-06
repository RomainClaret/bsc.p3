# -*- coding: utf-8 -*-

import tweaks
import common_functions
import part_of_speech

__author__ = "Romain Claret"
__maintainer__ = "Romain Claret"
__copyright__ = "Copyright 2015, Romain Claret "
__credits__ = ["Romain Claret"]

# Copyright (C) Romain Claret, All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
__license__ = "Proprietary and confidential"
__version__ = "1.0.0"
__email__ = "romain.claret@rocla.ch"
__status__ = "Prototype"  # Prototype, Development, Production
__date__ = "22.11.2015"


"""@package meaning_space
Documentation about the building of the meaning space, a normalized matrix of corpus
"""


def init_meaning_space():
    """
    Initialisation of the matrix of meanings
    Adding metadata information into the matrix of meanings
    """
    tweaks.base_matrix_of_meanings.sort(key=lambda s: (s[0].lower(), s))
    tweaks.matrix_of_meanings.append([])
    for element in tweaks.base_matrix_of_meanings:
        tweaks.matrix_of_meanings[0].append(element)


def build_meaning_space(word_list):
    """
    Building a Multidirectional Vectorial Space list of words
    :param word_list: vector of frequency words from a corpus
    :return:
    """
    for word in word_list:
        if word[0] not in tweaks.matrix_of_meanings[0]:
            tweaks.matrix_of_meanings[0].append(word[0])
    tweaks.matrix_of_meanings[0].sort(key=lambda s: (s[0].lower(), s))


def populate_meaning_matrix(word_list, index, filename):
    """
    Populate the meaning space matrix
    :param word_list: vector of frequency words from a corpus
    :param index: index in the matrix of meanings
    :param filename: name of the corpus
    """
    word_dict = convert_list_to_dict(word_list)
    tweaks.matrix_of_meanings.append([])

    for x in range(0, len(tweaks.base_matrix_of_meanings)):
        if tweaks.base_matrix_of_meanings[x] == "#emotion":
            tweaks.matrix_of_meanings[index + 1].append(0)
        elif tweaks.base_matrix_of_meanings[x] == "#length_total":
            tweaks.matrix_of_meanings[index + 1].append(0)
        elif tweaks.base_matrix_of_meanings[x] == "#wait_average":
            tweaks.matrix_of_meanings[index + 1].append(0)
        elif tweaks.base_matrix_of_meanings[x] == "#wait_total":
            tweaks.matrix_of_meanings[index + 1].append(0)

    for word in tweaks.matrix_of_meanings[0][len(tweaks.base_matrix_of_meanings):]:
        if word in word_dict.keys():
            tweaks.matrix_of_meanings[index + 1].append(word_dict[word])
        else:
            tweaks.matrix_of_meanings[index + 1].append(0)


def convert_list_to_dict(list):
    """
    Converter list to dictionary
    :param list: list to convert
    :return: dictionary equivalent
    """
    d = {}
    for key, value in list:
        d[key] = value
    return d


def convert_dict_to_list(dict):
    """
    Converter dictionary to list
    :param dict: dictionary to convert
    :return: list equivalent
    """
    l = []
    sorted_dict = sorted(dict.keys())
    for key in sorted_dict:
        l.append([key, dict[key]])
    return l


def display_matrix_of_meanings():
    """
    Display the representation of the matrix of meanings
    """
    for x in range(0, len(tweaks.matrix_of_meanings[0])):
        print(str(tweaks.matrix_of_meanings[0][x]) + " " + str(tweaks.matrix_of_meanings[1][x]) + " " + str(
                tweaks.matrix_of_meanings[2][x]))


def normalize_frequencies(frequencies):
    """
    Normalize the frequencies of the words in a vector. Calculate the occurrence / total words
    :param frequencies: list of frequencies
    :return: list of frequencies normalized
    """
    words_total = len(frequencies)
    tmp_frequencies = []

    for line in range(0, len(frequencies)):
        tmp_frequencies.append([frequencies[line][0], frequencies[line][1] / words_total])

    return tmp_frequencies


if __name__ == "__main__":
    """
    This function is run if this file is run directly.

    It will:
    Use the 2 first corpus in alphabetical order in the trainingCorpus folder.
    Initialize the matrix of meanings with the default meta data.
    Build the matrix of meanings with the words of corpus.
    Populate the matrix of meanings with the words of corpus frequencies.
    Display the matrix of meanings.
    """

    files_to_run = 2

    files = common_functions.getListFolders(tweaks.textFilesDirectory)

    init_meaning_space()

    for file in files[0:-len(files)+files_to_run]:
        f = open(tweaks.textFilesDirectory + file, encoding="utf-8")
        text = f.read()

        # remove non-ascii
        processed_string = "".join(i for i in text if ord(i) < 128)

        frequency = part_of_speech.get_words_frequency(processed_string, 0)

        build_meaning_space(frequency)
        f.close()

    for file in files[0:-len(files)+files_to_run]:
        f = open(tweaks.textFilesDirectory + file, encoding="utf-8")
        text = f.read()

        # remove non-ascii
        processed_string = "".join(i for i in text if ord(i) < 128)

        frequency = normalize_frequencies(part_of_speech.get_words_frequency(processed_string, 0))

        populate_meaning_matrix(frequency, files.index(file), file)

        f.close()

    for meaning in tweaks.matrix_of_meanings:
        print(meaning)
