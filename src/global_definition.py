'''
Created on Nov 7, 2018

@author: Giang Nguyen
@email: dexter.nguyen7@kaist.ac.kr

'''

import pandas as pd
import os.path
import pickle
import spacy

import en_core_web_sm
# spc = en_core_web_sm

DATA_PATH = '../Data/*/*'

# PARAMTER FILES FOR BOOSTING UP PROGRAM
PREP_PATH_2015 = '../output/preprocessed_list_2015.pkl'
VOCAB_PATH_2015 = '../output/vocabulary_2015.pkl'
PREP_PATH_2016 = '../output/preprocessed_list_2016.pkl'
VOCAB_PATH_2016 = '../output/vocabulary_2016.pkl'
PREP_PATH_2017 = '../output/preprocessed_list_2017.pkl'
VOCAB_PATH_2017 = '../output/vocabulary_2017.pkl'

DATASET_PATH_1 = '../output/dataset_1.txt'
DATASET_PATH_2 = '../output/dataset_2.txt'
OLLIE_OUTPUT_PATH_1 = '../output/ollie_tuples_1.txt'
OLLIE_OUTPUT_PATH_2 = '../output/ollie_tuples_2.txt'
OLLIE_POSTPROCESS_OUTPUT_PATH_1 = '../output/ollie_postprocess_tuples_1.txt'
OLLIE_POSTPROCESS_OUTPUT_PATH_2 = '../output/ollie_postprocess_tuples_2.txt'

DESCRIPTION_FILE = 'description.txt'

# PARAMETER FILE LISTS
PREP_FILE_LIST = [PREP_PATH_2015, PREP_PATH_2016, PREP_PATH_2017]
VOCAB_FILE_LIST = [VOCAB_PATH_2015, VOCAB_PATH_2016, VOCAB_PATH_2017]
DATA_FILE_LIST = [DATASET_PATH_1, DATASET_PATH_2]
OLLIE_FILE_LIST = [OLLIE_OUTPUT_PATH_1, OLLIE_OUTPUT_PATH_2]
OLLIE_POSTPROCESS_LIST = [OLLIE_POSTPROCESS_OUTPUT_PATH_1, OLLIE_POSTPROCESS_OUTPUT_PATH_2]
FILE_LIST = PREP_FILE_LIST + VOCAB_FILE_LIST

# COLUMNS OF DATAFRAME
TIME_STR  = ' time'
BODY_STR  = ' body'
AUTH_STR  = ' author'
SECT_STR  = ' section'
DESC_STR  = ' description'
TITL_STR  = 'title'
SPACE_STR = ' '

ART_TOKEN_STR = 'ART_IDX:'

# Confidence threshold is 0.6
JAVA_OLLIE_CMD_1 = 'java -Xmx2048m -jar ollie-app-latest.jar ../output/dataset_1.txt > ../output/ollie_tuples_1.txt -s'
JAVA_OLLIE_CMD_2 = 'java -Xmx2048m -jar ollie-app-latest.jar ../output/dataset_2.txt > ../output/ollie_tuples_2.txt -s'

JAVA_OLLIE_CMD_LIST = [JAVA_OLLIE_CMD_1, JAVA_OLLIE_CMD_2]

# INPUT MACROS
YES_STR_LIST = ['Y', 'y', 'YES', 'yes']
NO_STR_LIST = ['N', 'n', 'NO', 'no']

# Choose expected entities from this: https://spacy.io/usage/linguistic-features
#       organiztion countries people   events    date
ENTITY_TYPE = ['ORG', 'GPE', 'PERSON', 'EVENT', 'DATE']

# Name Entiry Recognition
spc = spacy.load('en')

docs_num  = 0
arts_nums = 0
vocabulary = []
docs = [list(), list(), list()]
vocab_size = 0
data = pd.DataFrame(columns=[])
data2015 = pd.DataFrame(columns=[])
data2016 = pd.DataFrame(columns=[])
data2017 = pd.DataFrame(columns=[])
'''''''''''''''''''''
    23769 articles
'''''''''''''''''''''
FIRST_YEAR  = 2015
SECOND_YEAR = 2016
THIRD_YEAR  = 2017
FOURTH_YEAR = 2018
YEARS = [FIRST_YEAR, SECOND_YEAR, THIRD_YEAR, FOURTH_YEAR]

K_MEANS_PARAM = 149
ISSUE_NUMBER = 2
