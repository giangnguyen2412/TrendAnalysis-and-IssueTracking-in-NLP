'''
Created on Nov 26, 2018

@author: Giang Nguyen
@email: dexter.nguyen7@kaist.ac.kr

'''

from global_definition import *
from text_process import *
from similarity import *

def removeDuplicateTuple(tuple_list):
    '''
    Remove redundancy, 0,75 (0.75 is an acceptable threshold get by experiments)
    is similarity threshold to remove the redundancy
    Use lines.copy() because we want to remove directly on lines variable
    :param: tuple_list: a list of lines as output of OLLIE but they are duplicated (list)
    :return: lines: a list of processed lines (list)
    '''

    lines = tuple_list
    lines_copy = lines.copy()
    for i in range(len(lines_copy)-1):
        if ((ART_TOKEN_STR not in (lines_copy[i]))):
            if (getStringSimilarityDegree(lines_copy[i], lines_copy[i+1]) > 0.75):
                lines.remove(lines_copy[i+1])

    return lines

def postprocessOllieOutput(path, idx):
    '''
    Read a file line by line and do postprocessing on Ollie output
    :param: filePath (string)
    :param: idx: index of topic. We are having two topics, idx is 0 or 1 (int)
    :return: lines: a list of processed lines containing only enablers tuples (list)
    :return: dictionary: a dictionary with key is article index. Each entry of
    the dictionary is a list of ollie tuples formatted (ei,r,ej,enabler). A dictionary of lists of lists
    '''

    dictionary = dict()
    art_idx = 0
    ollie_tuple = tuple()
    tuple_list = list()

    with open(path) as f:
        lines = [line.rstrip('\n') for line in f if ('enabler' in line or ART_TOKEN_STR in line)]

    lines = removeDuplicateTuple(lines)

    with open(OLLIE_POSTPROCESS_LIST[idx], 'a') as f:
        for i in range(len(lines)):
            if 'enabler' in lines[i]:
                ollie_tuple = parseTupleFromLine(lines[i])
                tuple_list.append(ollie_tuple)
            elif ART_TOKEN_STR in lines[i]:
                if (len(tuple_list) != 0):  # To avoid art_idx = 0 at initialization
                    dictionary[art_idx] = tuple_list
                art_idx = parseIndexFromLine(lines[i])
                if (-1 == art_idx):
                    continue
                tuple_list = list()         # Reset typle_list for the next article
            else:
                pass

            f.write(lines[i] + '\n')

        dictionary[art_idx] = tuple_list    # The last article index of file
        print(dictionary)
        print(len(dictionary))

    return lines, dictionary

def extractInforOllie(dataset, indexList, topic_idx):
    '''
    Open IE with OLLIE, postprocessing output of OLLIE also
    :param: dataset: Dataframe from raw dataset (dataframe)
    :param: indexList: A list of indices of a topic.
    :param: topic_idx: Index of topic. 0 or 1.
    Each list includes indices of articles in dataframe (list)
    :return: lines_list: A list including postprocessed data from OLLIE
    :return: dict_list: A list -> dictionaries -> a list -> a list
    '''

    lines_list = list()
    dict_list = list()

    data_str = ''
    # Over all articles of a topic
    for df_idx in (indexList):
        # Write the article index to text file
        article_idx_str = ART_TOKEN_STR + str(df_idx) + '.' + SPACE_STR + '\n'
        data_str += article_idx_str + dataset.ix[df_idx][BODY_STR] + SPACE_STR + '\n'
        data_str += '\n'

    deleteFile(DATA_FILE_LIST[topic_idx])
    with open(DATA_FILE_LIST[topic_idx], "w") as text_file:
        text_file.write("%s" %(data_str))
        # text_file.write("%s" % data_str.encode("utf-8"))

    deleteFile(OLLIE_FILE_LIST[topic_idx])

    # Run the JAVA app with 2GB of RAM
    os.system(JAVA_OLLIE_CMD_LIST[topic_idx])

    deleteFile(OLLIE_POSTPROCESS_LIST[topic_idx])
    lines_list, dict_list = postprocessOllieOutput(OLLIE_FILE_LIST[topic_idx], topic_idx)

    return lines_list, dict_list
