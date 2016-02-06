# -*- coding: utf-8 -*-

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
__date__ = "01.11.2015"


"""@package tweaks
This is the library of used variables across the scripts.

Useful for global tweaking on the project itself.
"""

"""
Used for the Speech to text
"""
languageAudioFR = "fr-fr"
languageAudioEN = "en"
showAllResults = False
unknownSentence = -1
networkError = -2
shouldTranslate = True

"""
Used for the Audio Treatment
"""
baseAudioFile = "audioRaw/"
outputDirectory = "audioProcessed/"
customParameters = "silence 1 0.3 1% 1 0.2 1% : newfile : restart"
manual_split_control = True

"""
Used for the Space of Meanings
"""
base_matrix_of_meanings = ["#emotion", "#length_total", "#wait_total", "#wait_average"]
matrix_of_meanings = []
top_matrix_of_meanings = []
textFilesDirectory = "trainingCorpus/"
top_values = 0
matrix_of_names = []

"""
Used for the K-Means algorithm and the classification of corpus
"""
clusters_list = 0
index_of_data_custering = 0
cluster_meaning = 0
cluster_name = 0
run_voice_recognition = True
run_part_of_speech = False
print_clusters_names = False
print_clusters_top_meanings = False
use_clusters_top_meanings_or_names = 0

"""
Used for the Serialization
"""
use_serialized_training = False
serialize_training = True
serialized_folder = "serializedData/"
serialized_matrix_of_meanings_file = "matrix_of_meanings.data"
serialized_clusters_file = "clusters.data"
serialized_audio_folder = "audioTranscripts/"
use_serialized_audio = False
serialize_audio = True

