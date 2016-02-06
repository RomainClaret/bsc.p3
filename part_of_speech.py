# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import common_functions
import tweaks

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
__date__ = "08.11.2015"

"""@package part_of_speech
Documentation about the part of speech process.
"""


def get_word_tag(treebank_tag):
    """
    Get only words in the Adjective, Verb, Noun, and Adverb category of the wordnet.
    :param treebank_tag: tag of the tokenization
    :return: wordnet symolic of the word, if not part of the willing category will return nothing
    """

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def get_words_frequency(string, top_values):
    """
    Gets the words frequency in a corpus
    :param string: corpus
    :param top_values: maximum of sorted values to return
    :return: list of frequencies of the word in there synset form
    """

    # import stop words from nltk corpus
    stop_words_en_nltk = list(stopwords.words('english'))

    # create additional stop words for puntuations and others
    stop_words_en_custom = ['.', ',', '\'', '!', '(', ')', ':', ';', '?', '--', '*', '[', ']', '``', str("''"),
                            '&', '\'ll', '\'ve', '\'s', '\'re', 'a', 'b', 'c',
                            'i', '\'i', 'this', 'n\'t', 'a', 'could', 'should', 'would', 'can', 'will', 'shall',
                            'there', 'it', 'also', 'in', 'the', 'many', 'by', 'an',
                            '1990s', 'the', '+', '-', '...', '=', '%', '#', '[hide]', '[edit]', '.jpg', '/',
                            'be.v.01', 'have.v.01', 'use.v.01', 'besides.r.02', 'analysis.n.01', 'categorization.n.03',
                            'vitamin_e.n.01', 'vitamin_c.n.01', 'include.v.01', 'such.s.01', 'many.a.01', 'order.n.01',
                            'episode.n.01', 'show.n.01', 'not.r.01', 'standard.n.01', 'survey.n.01', 'factor.n.01',
                            'first.a.01']
    until_number = 300
    stop_words_en_custom_numbers = []
    for value in [lambda i=i: i for i in range(until_number+1)]:
        stop_words_en_custom_numbers.append(str(value()))

    # add them together
    stop_words_en = stop_words_en_nltk + stop_words_en_custom + stop_words_en_custom_numbers

    words_list_tmp = word_tokenize(string.lower())
    words_list = []

    lemmatizer = WordNetLemmatizer()
    for word in nltk.pos_tag(words_list_tmp):
        tag = get_word_tag(word[1])
        if tag is not '':
            try:
                synset_word = wordnet.synsets(lemmatizer.lemmatize(word[0], pos=tag), pos=tag)[0]
                words_list.append(synset_word.name())
            except:
                pass

    processed_word_list = [word for word in words_list if word not in stop_words_en]

    text_obj = nltk.Text(processed_word_list)

    fd = FreqDist(text_obj)

    result = list(fd.items())

    if top_values is not 0:
        result.sort(key=lambda x: x[1], reverse=True)
        result = result[:top_values]
        return result

    else:
        return result


if __name__ == "__main__":
    """
    This function is run if this file is run directly.

    It will:
    Open the first corpus in alphabetical order
    Get the frequency
    Display the synset and its frequency
    """

    files = common_functions.getListFolders(tweaks.textFilesDirectory)
    f = open(tweaks.textFilesDirectory + files[0], encoding="utf-8")
    text = f.read()

    # remove non-ascii
    processed_string = "".join(i for i in text if ord(i) < 128)

    frequency = get_words_frequency(processed_string, 0)

    for word in frequency:
        print(word)

