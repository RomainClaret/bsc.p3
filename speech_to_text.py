# -*- coding: utf-8 -*-

from os import path
import speech_recognition as sr
import tweaks
import common_functions
import sys
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
__date__ = "01.11.2015"


"""@package speech_to_text
Use of the speech_recognition package (pip) for the Google Speech-to-Text

speech_recognition also work with Wit.ai, IBM Speech to Text, and AT&T Speech to Text.
Can be found at: https://pypi.python.org/pypi/SpeechRecognition
"""


def transcriptAudioFile(pathToFile, language):
    """
    Transcription of a specific file in a specific language
    :param pathToFile: path the audio file
    :param language: language used in the audio file
    :return:
    """

    # obtain full path to file in the same folder as this script
    WAV_FILE = path.join(path.dirname(path.realpath(__file__)), pathToFile)

    r = sr.Recognizer()
    with sr.WavFile(WAV_FILE) as source:
        audio = r.record(source)  # read the entire WAV file

    try:
        # for private API key 'r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")'
        return r.recognize_google(audio, language=language, show_all=tweaks.showAllResults)
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass


def transcriptProcessedFiles(folderName):
    """
    Transcription of all audio files present in a folder and fuse them. To be combined with the audio_splitter.
    :param folderName: folder name in the audioProcessed folder
    :return: transcript of the splited audio files
    """
    pathToFolder = tweaks.outputDirectory + folderName
    transcriptText = ""

    files = common_functions.getListFolders(pathToFolder)
    progressbarUnit = int(100 / len(files))
    totalProgressbar = 0

    language = common_functions.getLanguage(folderName)
    print("speech_to_text: " + folderName + " in " + language)

    pathToFolder_serialized = tweaks.serialized_folder + tweaks.serialized_audio_folder
    check_serialized_files = common_functions.getListFolders(pathToFolder_serialized)

    sys.stdout.write("Text-to-Speech in progress: " + str(totalProgressbar) + "%.")
    sys.stdout.flush()
    for file in files:
        if tweaks.use_serialized_audio:
            if folderName in check_serialized_files:
                load_file = open(pathToFolder_serialized + folderName, 'rb')
                transcriptText = pickle.load(load_file)
                load_file.close()
                print("Load Serialized.100%.Done")
                return transcriptText

        try:
            text = transcriptAudioFile(pathToFolder + "/" + file, language)
            if text is not None:
                transcriptText = transcriptText + " " + str(text)
        except:
            transcriptText = transcriptText + " " + str(text)

        totalProgressbar += progressbarUnit
        sys.stdout.write(str(totalProgressbar) + "%.")
        sys.stdout.flush()
    print("..Done")

    if tweaks.serialize_audio:
        output = open(tweaks.serialized_folder + tweaks.serialized_audio_folder + folderName, 'wb')
        pickle.dump(transcriptText[1:], output, -1)  # use of highest protocol available
        output.close()
        print(folderName + " is now serialized.")

    return transcriptText[1:]


if __name__ == "__main__":
    """
    This function is run if this file is run directly.

    It will:
    Transcribe the first sub-folder in the audioProcessing folder.
    Print the transcription
    """
    folders = common_functions.getListFolders(tweaks.outputDirectory)
    text = transcriptProcessedFiles(folders[0])
    print(text)
