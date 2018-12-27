'''
Created on Nov 7, 2018

@author: Giang Nguyen
@email: dexter.nguyen7@kaist.ac.kr

'''

import glob
import json
import pandas as pd

from global_definition import *

def readData(path):
    '''
    Read json data files
    :param: path: The relative path to the input dataset directory (string)
    :return: docs_num: The number of data files in dataset (int)
    :return: arts_nums: The number of articles in dataset (int)
    :return: df: The dataset in dataframe format (dataframe)
    '''

    files = glob.glob(path, recursive=True)
    docs_num = len(files)
    df = pd.DataFrame(columns=[])

    for file in files:
        with open(file, 'r') as f:
            raw = json.load(f)
            data_df = pd.DataFrame.from_dict(raw)
            df  = pd.concat([df, data_df], axis = 0, sort = True)

    # Sort articles by time for inter-depence detection
    df[TIME_STR] = pd.to_datetime(df[TIME_STR])
    df = df.sort_values(by = TIME_STR, ascending = True)

    arts_nums = df.shape[0]
    return docs_num, arts_nums, df

def getArticleHeadingsByIndex(index_list, dataset):
    '''
    Retrieves titles of articles referenced by index
    :param:
    index_list: indices corresponding to articles in dataset (list of integers)
    dataset (table): the raw data which was the foundation of preprocessing, term weighting and clustering
    :return: the titles of articles grouped into the cluster in which the articles belong,
    type: array of sets of strings
    '''

    headings = []

    for index in index_list:
        headings.append(dataset.ix[index][TITL_STR])

    return headings

def getArticleDescriptionsByIndex(index_list, dataset):
    '''
    Retrieves descriptions of articles referenced by index
    :param:
    index_list: indices corresponding to articles in dataset (list of integers)
    dataset: the raw data which was the foundation of preprocessing, term weighting and clustering (table)
    :return: descriptions: the descriptions of articles (array of sets of strings)
    '''

    descriptions = []

    for index in index_list:
        descriptions.append(dataset.ix[index][DESC_STR])

    return descriptions

def getArticleBodyByIndex(index_list, dataset):
    '''
    Retrieves body of articles referenced by index
    :param:
    index_list: indices corresponding to articles in dataset (list of integers)
    dataset: the raw data which was the foundation of preprocessing, term weighting and clustering (table)
    :return: articles: the article texts (array of sets of strings)
    '''

    articles = []

    for index in index_list:
        articles.append(dataset.ix[index][BODY_STR])

    return articles

def getArticleDatesByIndex(index_list, dataset):
    '''
    Retrieves dates of articles referenced by index
    :param:
    index_list: indices corresponding to articles in dataset (list of integers)
    dataset: the raw data which was the foundation of preprocessing, term weighting and clustering (table)
    :return: datess: the dates of articles (array of sets of strings)
    '''

    dates = []

    for index in index_list:
        dates.append(dataset.ix[index][TIME_STR])

    return dates


def sortArticlesByIndex(index_list, dataset):
    '''
    Sorts index_list by article date
    :param:
    index_list: indices corresponding to articles in dataset (list of integers)
    dataset: the raw data which was the foundation of preprocessing, term weighting and clustering (table)
    :return: sort: sorted index_list (list)
    '''

    dates = getArticleDatesByIndex(index_list, dataset)
    idx_date = zip(index_list, dates)

    sorted_by_second = sorted(idx_date, key=lambda tup: tup[1])
    print(list(zip(*sorted_by_second))[0])
