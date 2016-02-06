# -*- coding: utf-8 -*-

import tweaks
import speech_to_text
import common_functions
import meaning_space
import kmeans_nD
import part_of_speech
import audio_spliter
import pickle
import subprocess
import time

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
__date__ = "26.01.2016"


"""
The following section listen live to an audio file.
Do a speech to text on the fly.
And searches for the best cluster at the same time.
Gives the results live.
"""

def demo_of_the_presentation(filename, threshold_distance_of_meanings, playing_audio):
    """
    This is the demo function, what does it?
    It loads the serialized data
    Split the audio file
    Do a speech to text of each file and compare the vector with the meaning space
    Keep track of the real talk time during call
    """

    audio_spliter.splitAudioFile(filename)
    load_serialized_matrix_of_meanings()
    load_serialized_clusters()

    if tweaks.print_clusters_names:
        print_clusters_names()

    if tweaks.print_clusters_top_meanings:
        print_clusters_top_meanings()

    final_time = 0
    track_total_audio_parts = 0
    latest_top_context_detected = ""
    text = ""
    total_lenght_of_audio_file = subprocess.check_output("./sox/soxi -D " + tweaks.baseAudioFile + filename, shell=True)
    folder_name = filename.split(".", 1)[0]
    language = common_functions.getLanguage(folder_name)

    print()
    print("Demo starts here")
    if playing_audio:
        print("Launching the audio file with VLC")
        subprocess.Popen("/Applications/VLC.app/Contents/MacOS/VLC " + tweaks.baseAudioFile + filename + " &> /dev/null", shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=False)
        time.sleep(1)
    print()

    for audio_part in common_functions.getListFolders(tweaks.outputDirectory + folder_name):
        start_time = time.time()
        lenght_of_audio_file = subprocess.check_output(
            "./sox/soxi -D " + tweaks.outputDirectory + folder_name + "/" + audio_part, shell=True)
        track_total_audio_parts += float(lenght_of_audio_file)
        try:
            tmp_text = speech_to_text.transcriptAudioFile(tweaks.outputDirectory + folder_name + "/" + audio_part,
                                                          language)
            if tmp_text is not None:
                text += str(tmp_text) + " "
                print("Speech to text finished: \"" + str(tmp_text) + "\"")
            else:
                print("/!\\ Sorry, Google didn't understand this part.")
        except:
            print("An error occured during the speech to text process, do you have internet?")

        cleaned_string = "".join(i for i in text if ord(i) < 128)
        frequencies = meaning_space.normalize_frequencies(part_of_speech.get_words_frequency(cleaned_string, 0))
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

        file_clusters_distance = list(kmeans_nD.cos_cdist_clusters(tweaks.clusters_list, file_to_classify))
        distance_order = []
        for i in range(0, len(tweaks.clusters_list)):
            distance_order.append([file_clusters_distance[i], tweaks.cluster_name[i]])

        latest_top_context_detected = distance_order

        distance_order.sort(key=lambda x: x[0], reverse=False)
        distance_order = distance_order[:tweaks.top_values]

        for distance in distance_order:
            print(distance)

        elapsed_time = time.time() - start_time

        final_time += elapsed_time

        print("Process time for this part: " + str(format(elapsed_time, '.2f')))
        print("Original file length for this part: " + str(format(float(lenght_of_audio_file), '.2f')))
        different_of_time_process_real = float(lenght_of_audio_file) - elapsed_time
        if different_of_time_process_real < 0:
            if float(lenght_of_audio_file) <= 0.01:
                print("Process time is late on audio track of: " + str(format(different_of_time_process_real*(-1), '.2f')) + " seconds")
            else:
                percent_time_value = different_of_time_process_real/float(lenght_of_audio_file)
                print("Process time is late on audio track of: " + str(format(abs(percent_time_value), '.2f')) + "%")
        else:
            percent_time_value = different_of_time_process_real/float(lenght_of_audio_file)*100
            print("Process time is in advance on audio track of: " + str(format(percent_time_value, '.2f')) + "%")
        print("Total process time until now: " + str(format(final_time, '.2f')))
        print("Total calling time until now: " + str(format(track_total_audio_parts, '.2f')))
        print()

        # Waiting until the end of the audio length part to simulate the
        while float(lenght_of_audio_file) > elapsed_time:
            elapsed_time = time.time() - start_time

    latest_top_context_detected.sort(key=lambda x: x[0], reverse=False)
    context_output = [latest_top_context_detected[0][1][1]]
    for context in latest_top_context_detected[1:]:
        if (float(context[0]) - float(latest_top_context_detected[0][0])) <= threshold_distance_of_meanings:
            context_output.append(str(context[1][1]))

    print()
    print("Audio file length: " + str(format(float(total_lenght_of_audio_file), '.2f')) + " seconds")
    print("Process time of demo: " + str(format(float(final_time), '.2f')) + " seconds")

    different_of_time_process_real = float(total_lenght_of_audio_file) - final_time
    if different_of_time_process_real <= 0:
        percent_time_value = different_of_time_process_real/float(total_lenght_of_audio_file)
        print("Total Process time is late on audio track of: " + str(format(abs(percent_time_value), '.2f')) + "%")
    else:
        percent_time_value = different_of_time_process_real/float(total_lenght_of_audio_file)*100
        print("Process time is ahead on audio track of: " + str(format(percent_time_value, '.2f')) + "%")

    if len(context_output) > 1:
        print("Contexts extracted within " + str(threshold_distance_of_meanings) + " of meaning threshold: " + str(context_output))
    elif len(context_output) == 1:
        print("Context extracted within " + str(threshold_distance_of_meanings) + " of meaning threshold: " + str(context_output))
    else:
        print("Could not extract any context of the audio file. Sorry?")


"""
The following section is about the serialization of the data
"""


def load_serialized_matrix_of_meanings():
    """
    Load the matrix of meanings from the serializedData folder.
    """
    print("Loading serialized matrix_of_meanings...")
    load_file = open(tweaks.serialized_folder + tweaks.serialized_matrix_of_meanings_file, 'rb')
    tweaks.matrix_of_meanings = pickle.load(load_file)
    load_file.close()


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


if __name__ == "__main__":
    """
    Options about the serialization of the data
    """
    tweaks.serialize_audio = False
    tweaks.use_serialized_training = True
    tweaks.use_serialized_audio = True

    """
    Options about the customization of the training
    """
    tweaks.use_clusters_top_meanings_or_names = 1  # 0 for top_meanings, 1 for names
    tweaks.top_values = 3

    """
    Options about the display of the data
    """
    tweaks.print_clusters_names = False
    tweaks.print_clusters_top_meanings = False

    """
    Options about the demo itself
    """
    threshold_distance_of_meanings = 0.02
    playing_audio = True

    """
    School Splash Screen + Application name
    """
    print()
    common_functions.splash_screen_arc()
    print()
    print("Manager of Emergency Calls by Romain Claret")
    print("Made for the 1st semester of the 3rd year DLM at HE-ARC Engineering School Neuchatel")
    print()
    print("Demonstration Program for Defense Project Presentation")
    print()
    print()

    """
    Execution of the demo programme
    Provide the name with the extension of the audio file from audioRaw
    """
    demo_of_the_presentation("en-arlington-heights-drowning.wav", threshold_distance_of_meanings, playing_audio)
    #demo_of_the_presentation("en-jersey-city-fire.wav", threshold_distance_of_meanings, playing_audio)
    #demo_of_the_presentation("en-orlando-kidnapping.wav", threshold_distance_of_meanings, playing_audio)
    #demo_of_the_presentation("en-metrolink-crash.wav", threshold_distance_of_meanings, playing_audio)
    #demo_of_the_presentation("en-wheelchair.wav", threshold_distance_of_meanings, playing_audio)
