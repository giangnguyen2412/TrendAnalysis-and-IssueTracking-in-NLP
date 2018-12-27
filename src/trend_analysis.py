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
from text_process import *
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

    #open file to write feature selection
    f = open("feature_selection.txt", "w")

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

    file = open("top_ten.txt", "w")

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

        # OPTION 1: feature selection by variance threshold ------------------------------

        # # compute occurrence matrix
        # occ_mtx = get_occurrence_matrix(preprocessed_list)

        # selected = feature_selection_variance(occ_mtx, .996)

        # # get selected vocabulary list
        # selected_voc = get_selected_vocab(selected, occ_mtx, vocabulary)
        # # get removed vocabulary list
        # removed = [x for x in vocabulary if x not in selected_voc]

        # # create vector space model by term weighting, this can be used for clustering
        # vector_space = tf_idf(selected)


        # OPTION 2: feature selection by df ----------------------------------------------

        # copmute vector space model by tf_idf, this can be used for clustering
        # feature selection by document frequency can be controlled by 2nd parameter
        vector_space, selected_voc = tf_idf_select(preprocessed_list, 0.001)

        # get removed vocabulary list
        removed = [x for x in vocabulary if x not in selected_voc]

        # OPTION 3: feature selection by LSA ---------------------------------------------
        # # TODO
        # vector_space, selected_voc = tf_idf_select(preprocessed_list, 0)
        # selected = dimensionality_reduction_LSA(vector_space, 100)

        # print(selected)

        # print to see result of feature selection
        f = open("feature_selection.txt", "a")
        print("vocabulary length:", len(vocabulary))
        f.write("vocabulary length: {}\n\n".format(len(vocabulary)))
        f.write(str(vocabulary))


        print("vocabulary length after feature selection:", len(selected_voc))
        f.write("\n\nvocabulary length after feature selection:{}\n\n".format(len(selected_voc)))
        f.write(str(selected_voc))

        print("vocabulary removed by feature selection:", len(removed))
        f.write("\n\nvocabulary removed by feature selection:{}\n\n".format(len(removed)))
        f.write(str(removed))


        #########################################
        ######## WEIGTING AND CLUSTERING ########
        #########################################

        # performs the clustering, parameters: 1. number of clusters to be created, 2. the tf_idf_matrix, 3. number of iterations the clustering should perform,
        #                                      4. the terms, 5. the raw data, 6. wether the clustering should be tested or not
        # top_ten (array of tuples(x, y) of integers): the indices of the top ten clusters and the number of articles in them
        # top_ten_headings (array of sets of strings): the titles of the articles belonging to one of the top ten clusters, matched to the cluster
        # top_ten_vocabulary (array of sets of strings): the terms of the articles belonging to one of the top ten clusters, matched to the cluster
        top_ten, top_ten_headings, top_ten_vocabulary = kMeansClustering(K_MEANS_PARAM, vector_space, 100, selected_voc, dataset, False)

        file.write("year ")
        file.write(str((year_index + 2015)))
        file.write(":\n")
        printTopTenToFile(file, top_ten_headings, top_ten_vocabulary)
        file.write("\n\n\n\n\n")

        print('Trend Analysis done for year %d' %(YEARS[year_index]))
        input("Press Enter to continue...")

    stop = timeit.default_timer()
    # print('Eslaped Time: ', stop - start)

    input("Press Enter to exit...")
if __name__ == '__main__':
    main()
