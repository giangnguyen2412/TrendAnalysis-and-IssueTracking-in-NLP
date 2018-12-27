'''
Created on Nov 7, 2018

@author: Giang Nguyen
@email: dexter.nguyen7@kaist.ac.kr

'''

import glob
import os
import nltk
import itertools
import numpy as np
import copy

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words as nltk_words
from time import sleep

from collections import Counter
from global_definition import *
from text_process import *
from progress_bar import *

porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))

vocabulary = []
vocab_size = 0

# Uncomment this if you haven't download these packages yet
'''
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
'''

word_list = set(nltk_words.words())

def preprocess(text):
    '''
    Preprocess raw text to get tokens
    :param: text: Input text (string)
    :return: vocab_entries: Output vocabulary (filter)
    '''

    stemmed = []
    lemmatized = []
    wordsFiltered = []

    # Normalization
    text = text.lower()

    # Tokenization
    token_text = nltk.word_tokenize(text)

    # Lemmatization
    for token in token_text:
        lemmatized.append(wordnet_lemmatizer.lemmatize(token))

    wordsFiltered = filter(lambda word_to_filter: word_to_filter not in stopWords and word_to_filter.isalpha() and word_to_filter in word_list, lemmatized)

    vocab_entries = wordsFiltered
    return vocab_entries

def countDocuments(arts_nums, data):
    '''
    Count the number of documents by three year groups: 2015, 2016 and 2017 + 2018
    :param: arts_nums: The number of articles in dataset (int)
    :param: data: Input dataset in dataframe format (dataframe)
    :return: data_cnt: Numbers of articles for 3 years (list)
    '''

    data_cnt = [0, 0, 0, 0]    # The number of articles for 2015 2016 2017 and 2018 respectively
    for art_index in range(arts_nums):
        for year_index in range(len(YEARS)):
            if(YEARS[year_index] == data.ix[art_index][TIME_STR].year):
                data_cnt[year_index] +=1
                break
    data_cnt[2] += data_cnt[3]     # We combine 2017 and 2018
    print('2015: %d articles| 2016: %d articles| 2017 and 2018: %d articles' %(data_cnt[0], data_cnt[1], data_cnt[2]))
    return data_cnt

def separateDataSet(data_cnt, data):
    '''
    Separate dataset by three year groups: 2015, 2016 and 2017 + 2018
    :param: data_cnt: Numbers of articles for 3 years (list)
    :param: data: Input dataset in dataframe format (dataframe)
    :return: data_list: Three sets of articles for 3 years (list)
    '''

    global data2015, data2016, data2017
    # Create data frames from sorted dataframe
    data2015 = data.ix[0:data_cnt[0]].copy()
    data2016 = data.ix[data_cnt[0]:data_cnt[0] + data_cnt[1]].copy()
    data2017 = data.ix[data_cnt[0] + data_cnt[1]:].copy()

    data_list = [data2015, data2016, data2017]
    return data_list

def getToken(dataset, data_cnt, year_index):
    '''
    Get tokens from documents of one year
    :param: dataset: Input dataset in dataframe format for just one year (dataframe)
    :param: data_cnt: Numbers of articles for just one year (int)
    :param: year_index: The year of articles. E.g. 2015, 2016 or 2017 (int)
    :return: vocabulary: The output tokens, entries are unique (list)
    :return: prep_list: The output tokens, entries are not unique (list)
    '''

    global docs
    # data_str = ''
    vocabulary = []
    prep_list = []

    l = data_cnt[year_index]
    # l = 100
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50) # Initial call to print 0% progress

    for art_index in range(data_cnt[year_index]):         # Run for all articles
    # for art_index in range(100): # Enable this and disable above FOR-LOOP for testing
        tokens = preprocess(dataset.ix[art_index][BODY_STR])

        # create a deep copy of the token list
        tokens_list = list(copy.deepcopy((tokens)))

        # concatenate tokens of an article
        prep_list.append(" ".join(tokens_list))

        docs[year_index].append(dataset.ix[art_index][BODY_STR])

        # add tokens to vocabulary ensuring that there are no duplicates
        for token in list(tokens):
            if token not in vocabulary:
                vocabulary.append(token)

        # update status bar
        sleep(0.1)
        printProgressBar(art_index + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50) # Update Progress Bar

    # Delete exsiting files first
    deleteFile(PREP_FILE_LIST[year_index])
    deleteFile(VOCAB_FILE_LIST[year_index])

    # Then write new files using pickle to load later
    with open(PREP_FILE_LIST[year_index], 'wb') as f:
        pickle.dump(prep_list, f)

    with open(VOCAB_FILE_LIST[year_index], 'wb') as f:
        pickle.dump(vocabulary, f)

    return vocabulary, prep_list
