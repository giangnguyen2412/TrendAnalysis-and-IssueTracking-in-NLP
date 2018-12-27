'''
Created on Nov 7, 2018

'''

import pandas as pd
import timeit

from clustering import *
from global_definition import *
from preprocess import *
from read_data import *
from term_weighting import *
from similarity import *
from ner_spacy import *
from openie_ollie import *
from text_process import *
from inter_dependency import *
from visualization import visualizeInterDependency
from progress_bar import printProgressBar
from time import sleep

def main():
    start = timeit.default_timer()

    global docs_num
    global arts_nums
    global data
    global vocabulary
    global vocab_size
    global docs

    docs_num, arts_nums, data = readData(DATA_PATH)  # 0.7s
    print('Total files:', docs_num)
    print('Total articles:', arts_nums)

    data_cnt = [0, 0, 0, 0]    # The number of articles for 2015 2016 2017 and 2018 respectively
    data_cnt = countDocuments(arts_nums, data)  # 12s
    data_list = separateDataSet(data_cnt, data)

    # existFlag for checking existence of all plk files
    existFlag = False
    # boostFlag for cheking using pkl files or not
    boostFlag = False

    # If dataset changes, pkl files will not match, be careful!!!
    existFlag = checkFileExistence(FILE_LIST)
    if (True == existFlag):
        intent = input('The program parameters are available! Would you like to use them to speed up program? Y/N?')
        if (intent in YES_STR_LIST):
            boostFlag = True
        elif (intent in NO_STR_LIST):
            boostFlag = False
        else:
            print('Ambiguous input! Program is going to be terminated!')
            return

    # concatenate token list of all years
    prep_lists = list()

    for year_index in range(len(data_list)):     # Run for each year
        dataset = data_list[year_index]
        # Use available pkl files
        if (True == boostFlag):
            with open(PREP_FILE_LIST[year_index], 'rb') as f:
                preprocessed_list = pickle.load(f)

            with open(VOCAB_FILE_LIST[year_index], 'rb') as f:
                vocabulary = pickle.load(f)
        # Run normally without using existing parameter files
        else:
            vocabulary, preprocessed_list = getToken(dataset, data_cnt, year_index)

        prep_lists.extend(preprocessed_list)

    d = open(DESCRIPTION_FILE, "r")
    descriptions = d.readlines()

    # for d in descriptions:
    for i in range(ISSUE_NUMBER):
        d = descriptions[i]
        num_docs_cluster = int(d.partition("[")[2].partition("]")[0])
        description = d.partition("]")[2]
        topic_index = descriptions.index(d)

        # perform similarity query
        similar = getSimilarDocuments(prep_lists, description, K_MEANS_PARAM, num_docs_cluster)

        # extract triples
        lines_list, dict_list = extractInforOllie(data, similar, topic_index)

        # get linked articles
        linked = getInterdependent(data, similar, dict_list)
        visualizeInterDependency(linked, data, similar, d)
        input("Press Enter after saving the plot...\n")

    stop = timeit.default_timer()
    # print('Eslaped Time: ', stop - start)

    input("Press Enter to exit...")
if __name__ == '__main__':
    main()
