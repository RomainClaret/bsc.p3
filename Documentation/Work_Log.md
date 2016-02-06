# Worklog
- Project Name: Manager of emergency calls
- N° Project: 16INF-TA221
- Author: Claret Romain
- Teacher: Ghorbel Hatem
- Language: Python
- Abstract: Development of an application of the on-the-fly analyse and classification of emergency calls from emergency services.

## Week 34
- First contact with Mr. Hobi (Chef du service de la Sécurité Urbaine)
- Result of the emails: No data can be retrieved because it's confidential

## Week 38
- Making specifications
- Start playing with the tool NLTK
- Calling Mr Viuille, Chef CET, for a RDV

## Week 39
- Playing with the tool NLTK
- Gathering information about where to obtain raw call recordings
- RDV with Mr Viuille, he said that it's a promising project
- Obtained some statistics from the emergency calls
- Contacted Ms. Virginie Fasel Lauzon, the person who has some anonymised raw audio data

## Week 40
- Finishing up and Submitting the specifications
- Recommendations for voice recognition: Htk and Sphinx
- Contacting Ms. Waelchli concerning the anonymised raw audio data

## Week 41
- Making of 4 fake police audio records
- Testing different APIs for the voice recognition
- Trying to install Htk and Sphinx
- Contacting Ms. Eva Roos concerning the anonymised raw audio data

## Week 42
- Response from Ms. Virginie Fasel Lauzon concerning the anonymised raw audio data
- Htk is not good for this project, because with want something integrated in python
- Trying to install Sphinx

## Week 43
- Looks like we won't have any raw data for audio calls...
- SphinxCmu in python is a pain to install...

## Week 44
- Tests to install sphinx is an epic fail...
- Looking for alternatives to voice recognition
- Test of Dragon Dictate
- Test of Apple Voice Recognition
- Google is the best....

## Week 45
- Tweaking the google api for recognition

## Week 46
- Manually cutting audio files because the size limit of google is 15 seconds...
- Using google api to translate an entire audio
- Doing part-of-speech with TestBlob

## Week 47
- Audio file splitter at silences
- Transcript splitter audio files with Google API
- Part of speech for the transcripted audio files with TextBlob
- It's pretty bad at the moment... The meaning is sometimes deteriorated.. It needs tweaking..

## Week 48
- Creating the work log from emails and notes
- Starting working on the Multi-directional Vectorial Space


## Week 49
- Working on the Multi-directional Vectorial Space
- Errors with the TextBlob tokens, and Lemmatize

## Week 50
- Working keyword extractor from a text
 - Use of frequency distribution and stop word filters from NLTK
- Working Naive Bayes Classifier for positive and negative sentences with training
- Turn down of the offer of Ms. Virginie Fasel Lauzon concerning the anonymised raw audio data (TP+TB)

## Week 52
- Bug-fix for the character with the wrong encoding in texts (from widipedia)
- Working on words' classification in a multidirectional vectorial space

## Week 53
- Automated build of the matrix of meanings

## Week 1
- Worked onget_match_ranking(list_a,list_b) and got canceled for get_match_cosinus
- Frequencies of words are normalized
- Working 1st version of K-means with cluster number choice
- Optimised populate_meaning_matrix for if conditions
- Added: Wikipedia dumps for emergency meanings
- Auto reading from all files and building a kmeans clusters

## Week 2
- Made folder structure in the repository
- Working on the report

## Week 3
- K-Means is now mastered!
- Serialization of the data
- Switched to NLTK instead of TextBlob
- Fusing all the functions to build the app. Results are great :)
- Working finished the rapport.
- Cleaning the source code and commenting.
- Turning the source codes + rapport + required annexes
