'''
Created on Nov 28, 2018

@author: Giang Nguyen
@email: dexter.nguyen7@kaist.ac.kr

'''

import glob
import os
import nltk
import itertools
import numpy as np
import copy

from collections import Counter
from global_definition import *
from progress_bar import *

def parseIndexFromLine(line):
    '''
    Parse the article index from string
    :param: line: a line containing the index string with format: ART_IDX:index_number (string)
    :return: index: index of article (int)
    '''

    s = (line.split(':')[1]).split('.')[0]
    try:
        index = int(s)
    except ValueError:
        return -1

    return index

def parseTupleFromLine(line):
    '''
    Parse ollie tuple from string
    :param: line: a line containing the index string with format: ART_IDX:index_number (string)
    :return: ollie_tuple: a tuple containing entity i, relation, entiry j, enabler (tuple)
    '''

    line_str = line.split(':')[1]    # To separate out from confidence score
    c = line_str.split('[')          # To separate enabler and (ei,r,ej)
    enabler = c[1].split(']')[0]
    tup_str = c[0].split(';')
    ei = tup_str[0].split('(')[1]
    r = tup_str[1]
    ej = tup_str[2].split(')')[0]

    ollie_tuple = (ei,r,ej,enabler)
    return ollie_tuple

def checkFileExistence(fileList):
    '''
    Check file existence or not
    :param: fileList (list)
    :return: True if all files in list are existing, False otherwise (boolean)
    '''

    if all([os.path.isfile(f) for f in fileList]):
        return True
    else:
        return False

def deleteFile(filePath):
    '''
    Delete a file located in filePath
    :param: filePath (string)
    :return: None
    '''

    ## If file exists, delete it ##
    if os.path.isfile(filePath):
        os.remove(filePath)
    else:
        print("%s file not found" % filePath)
