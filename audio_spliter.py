# -*- coding: utf-8 -*-

import os
import tweaks
import common_functions

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
__date__ = "15.11.2015"

"""@package audio_spliter
Documentation for the module using SoX for audio manipulation.

Algorithms here are using SoX: http://sox.sourceforge.net
Information about tweaking can be found: http://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/
"""


def splitAudioFiles(number_of_iterations=None):
    """
    Function that splits all audio files available at silences. And makes a folder containing the part of the file.
    Used mainly to distribute the load for the Google Speech Recognition, 15 seconds.
    It also simulate the real time communication by cutting the buffer at respiration of the speaker.

    :param number_of_iterations: maximum amount of files to process
    """

    count = 0

    os.system("rm -r " + tweaks.outputDirectory + "*")

    for file in common_functions.getListFolders(tweaks.baseAudioFile):
        print("audio splitting: " + file + " and the language is: " + common_functions.getLanguage(file))
        foldername = file.split(".", 1)[0]
        os.system("mkdir " + tweaks.outputDirectory + foldername + " &> /dev/null")
        os.system(
                "./sox/sox " + tweaks.baseAudioFile + file + " " + tweaks.outputDirectory + foldername + "/" + file +
                " " + tweaks.customParameters + " &> /dev/null")
        if number_of_iterations is not None:
            count += 1
            if count >= number_of_iterations:
                break


def splitAudioFile(file):
    """
    Function that splits an audio file at silences. And makes a folder containing the part of the file.
    Used mainly to distribute the load for the Google Speech Recognition, 15 seconds.
    It also simulate the real time communication by cutting the buffer at respiration of the speaker.
    :param file: Name of the file
    """
    foldername = file.split(".", 1)[0]
    os.system("rm -r " + tweaks.outputDirectory + foldername)

    print("audio splitting: " + file + " & language is: " + common_functions.getLanguage(file))
    os.system("mkdir " + tweaks.outputDirectory + foldername + " &> /dev/null")
    os.system(
            "./sox/sox " + tweaks.baseAudioFile + file + " " + tweaks.outputDirectory + foldername + "/" + file +
            " " + tweaks.customParameters + " &> /dev/null")


if __name__ == "__main__":
    """
    This function is run if this file is run directly.

    It will cut at silences all files present in the audioRaw folder and save them into a sub folder with its name in the audioProcessed folder.
    Files will have a suffix with 3 numbers, which indicates their order.
    """
    splitAudioFiles()
