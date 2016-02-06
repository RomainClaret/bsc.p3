# -*- coding: utf-8 -*-

import tweaks
import speech_to_text
import common_functions
import meaning_space
import kmeans_nD
import part_of_speech
import audio_spliter
import pickle

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
__date__ = "21.01.2016"

"""@package main
Global documentation for the use of the application.
"""

"""
The following section is about the Voice Recognition
"""


def section_voice_recognition(toggle, max_files=None, filename=None):
    if toggle:
        if max_files is None:
            max_files = len(common_functions.getListFolders(tweaks.baseAudioFile))

        if tweaks.manual_split_control:
            audio_spliter.splitAudioFiles(max_files)

        count = 0

        for fileFolder in common_functions.getListFolders(tweaks.outputDirectory):
            if filename is None:
                text_transcripted = speech_to_text.transcriptProcessedFiles(fileFolder)
                section_part_of_speech(tweaks.run_part_of_speech, True, text_transcripted, None, fileFolder)
                count += 1
                if count >= max_files:
                    return True
            elif filename == fileFolder:
                text_transcripted = speech_to_text.transcriptProcessedFiles(fileFolder)
                section_part_of_speech(tweaks.run_part_of_speech, True, text_transcripted, None, fileFolder)
                return True

        return True

"""
The following section is about the serialization of the data
"""


def serialize_matrix_of_meanings():
    """
    Serialize the matrix of meanings into the serializedData folder.
    """
    print("Serialization of the matrix_of_meanings...")
    output = open(tweaks.serialized_folder + tweaks.serialized_matrix_of_meanings_file, 'wb')
    pickle.dump(tweaks.matrix_of_meanings, output)  # use of highest protocol available
    output.close()


def load_serialized_matrix_of_meanings():
    """
    Load the matrix of meanings from the serializedData folder.
    """
    print("Loading serialized matrix_of_meanings...")
    load_file = open(tweaks.serialized_folder + tweaks.serialized_matrix_of_meanings_file, 'rb')
    tweaks.matrix_of_meanings = pickle.load(load_file)
    load_file.close()


def serialize_clusters():
    """
    Serialize the clusters into the serializedData folder.
    """
    print("Serialization of the cluster_meaning...")
    output = open(tweaks.serialized_folder + tweaks.serialized_clusters_file, 'wb')
    pickle.dump(tweaks.cluster_meaning, output, -1)  # use of highest protocol available
    pickle.dump(tweaks.cluster_name, output, -1)
    pickle.dump(tweaks.clusters_list, output, -1)
    pickle.dump(tweaks.index_of_data_custering, output, -1)
    output.close()


def load_serialized_clusters():
    """
    Load the clusters from the serializedData folder.
    """
    print("Loading serialized cluster_meaning...")
    load_file = open(tweaks.serialized_folder + tweaks.serialized_clusters_file, 'rb')
    tweaks.cluster_meaning = pickle.load(load_file)
    tweaks.cluster_name = pickle.load(load_file)
    tweaks.clusters_list = pickle.load(load_file)
    tweaks.index_of_data_custering = pickle.load(load_file)
    load_file.close()


"""
The following section is about the training of the Part of speech
"""


def print_clusters_top_meanings():
    """
    Display an amount of top keywords related to the clusters defined by top_values.
    """
    for cluster in tweaks.cluster_meaning:
        print(cluster)


def print_clusters_names():
    """
    Display the name of corpus related to the clusters.
    """
    for cluster in tweaks.cluster_name:
        print(cluster)


def section_part_of_speech_training(number_of_clusters, files=None):
    """
    This section trains the part of speech by creating clusters of meanings.
    :param number_of_clusters: number of cluster targeted
    :param files: list of corpus to classify. If not specified, all corpus available will be used
    """

    meaning_space.init_meaning_space()
    if files is None:
        files = common_functions.getListFolders(tweaks.textFilesDirectory)

    for file in files:
        f = open(tweaks.textFilesDirectory + file, encoding="utf-8")
        text = f.read()

        tweaks.matrix_of_names.append(file[:-4])

        # remove non-ascii
        processed_string = "".join(i for i in text if ord(i) < 128)

        frequency = part_of_speech.get_words_frequency(processed_string, 0)

        meaning_space.build_meaning_space(frequency)
        f.close()

    for file in files:
        f = open(tweaks.textFilesDirectory + file, encoding="utf-8")
        text = f.read()

        # remove non-ascii
        processed_string = "".join(i for i in text if ord(i) < 128)

        frequency = meaning_space.normalize_frequencies(part_of_speech.get_words_frequency(processed_string, 0))
        tweaks.top_matrix_of_meanings.append(part_of_speech.get_words_frequency(processed_string, top_values))

        meaning_space.populate_meaning_matrix(frequency, files.index(file), file)

        f.close()

    tweaks.clusters_list = kmeans_nD.get_clusters_centroids(tweaks.matrix_of_meanings[1:], number_of_clusters)
    tweaks.index_of_data_custering = kmeans_nD.get_index_assign_data_to_cluster(tweaks.matrix_of_meanings[1:],
                                                                                tweaks.clusters_list)

    cluster_meaning_tmp = [[i] for i in range(number_of_clusters)]
    cluster_names_tmp = [[i] for i in range(number_of_clusters)]

    # append cluster_number and top_values of the related file
    for n in range(0, len(tweaks.index_of_data_custering)):
        for meaning in tweaks.top_matrix_of_meanings[n]:
            cluster_meaning_tmp[tweaks.index_of_data_custering[n]].append(meaning[0])

    for n in range(0, len(tweaks.index_of_data_custering)):
        cluster_names_tmp[tweaks.index_of_data_custering[n]].append(tweaks.matrix_of_names[n])

    tweaks.cluster_meaning = []
    for cluster in cluster_meaning_tmp:
        for name in cluster:
            if cluster.count(name) > 1:
                cluster.remove(name)
        tweaks.cluster_meaning.append(cluster)

    tweaks.cluster_name = []
    for cluster in cluster_names_tmp:
        tweaks.cluster_name.append(cluster)

"""
The following section is about the use of the Part of speech
"""


def section_part_of_speech(toggle, voice=False, audio_to_compare=None, file_to_compare=None, fileFolder=None):
    """
    This section will try to listen to an audio or text file to extract the corpus and then match it to the knowledge
    database.
    :param toggle: specify if the voice recognition should be speech should be running
    :param voice: specify the use of an audio file
    :param audio_to_compare: corpus
    :param file_to_compare: specify name of file if used
    :param fileFolder: name of the processed directory
    """

    if toggle:
        if not voice:
            if file_to_compare is None:
                file_to_compare = "wikipedia-intelligence.txt"

            f = open(tweaks.textFilesDirectory + file_to_compare, encoding="utf-8")
            text = f.read()
            f.close()
        else:
            file_to_compare = "the audio file"
            text = audio_to_compare

        if fileFolder is not None:
            file_to_compare = fileFolder

        # remove non-ascii
        processed_string = "".join(i for i in text if ord(i) < 128)

        frequencies = meaning_space.normalize_frequencies(part_of_speech.get_words_frequency(processed_string, 0))

        file_to_classify = []

        for element in tweaks.matrix_of_meanings[0]:
            count = 0
            for frequency in frequencies:
                if frequency[0] == element:
                    file_to_classify.append(frequency[1])
                    count += 1
                    break
            if count == 0:
                file_to_classify.append(0)

        if not frequencies:
            print("The speech_to_text process of " + str(
                    file_to_compare) + " has failed. Try again, or delete the audio source because it is too noisy.")
        else:
            print("The cos distance of " + str(file_to_compare) + " with the clusters is: [distance], [cluster]")
            file_clusters_distance = list(kmeans_nD.cos_cdist_clusters(tweaks.clusters_list, file_to_classify))
            distance_order = []
            for i in range(0, len(tweaks.clusters_list)):
                if tweaks.use_clusters_top_meanings_or_names == 0:
                    distance_order.append([file_clusters_distance[i], tweaks.cluster_meaning[i]])
                else:
                    distance_order.append([file_clusters_distance[i], tweaks.cluster_name[i]])

            distance_order.sort(key=lambda x: x[0], reverse=False)
            distance_order = distance_order[:3]

            for distance in distance_order:
                print(distance)
            print()


if __name__ == "__main__":
    """
    This function is run if this file is run directly.

    It will:
    Configure the procedures of execution such as the use of the serialization, the number of clusters, display, etc.
    Serialize data on the go if specified.
    Run or load the training the of corpus.
    Run or load audio recognition.
    Classify the audio files with the current knowledge of the application.
    Give results in a lab reading point of view.
    """

    """
    Options about the use of the main sections
    """
    tweaks.run_voice_recognition = False
    tweaks.run_part_of_speech = True

    """
    Options about the serialization of the data
    """
    tweaks.serialize_training = True
    tweaks.serialize_audio = True
    tweaks.use_serialized_training = False
    tweaks.use_serialized_audio = True

    """
    Options about the use of the audio file splitter
    """
    tweaks.manual_split_control = False

    """
    Options about the display of the data
    """
    tweaks.print_clusters_names = True
    tweaks.print_clusters_top_meanings = False

    """
    Options about the customization of the training
    """
    tweaks.use_clusters_top_meanings_or_names = 1  # 0 for top_meanings, 1 for names
    max_audio_files_to_transcribe = 5  # None for all # sorted order of the audioRaw folder
    number_of_clusters = 75

    top_values = 3
    file_to_compare = "wikipedia-fire.txt"

    """
    School Splash Screen + Application name
    """
    print()
    common_functions.splash_screen_arc()
    print()
    print("Manager of Emergency Calls by Romain Claret")
    print("Made for the 1st semester of the 3rd year DLM at HE-ARC Engineering School Neuchatel")
    print()
    print()

    """
    Execution of the main programme
    """
    print("Training of the part of speech in progress...")
    if tweaks.use_serialized_training:
        load_serialized_matrix_of_meanings()
        load_serialized_clusters()
    else:
        section_part_of_speech_training(number_of_clusters)
        if tweaks.serialize_training:
            serialize_matrix_of_meanings()
            serialize_clusters()

    if tweaks.print_clusters_names:
        print_clusters_names()

    if tweaks.print_clusters_top_meanings:
        print_clusters_top_meanings()

    print("Done Training")
    print()
    section_voice_recognition(tweaks.run_voice_recognition, max_audio_files_to_transcribe)

