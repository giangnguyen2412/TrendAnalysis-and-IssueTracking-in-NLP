from gensim import corpora, models, similarities
import pandas
from preprocess import preprocess
from difflib import SequenceMatcher

def getSimilarDocuments(prep_list, query, num_topics, num_docs):
    '''
    Obtain num_docs documents similar to query
    :param:
    prep_list: preprocessed document (list of strings)
    query: cluster description (string),
    num_topics: number of clusters in document collection (integer)
    num_docs: desired number of documents to return (integer)
    :return:
    sims: indices of documents similar to query (list of integers)
    '''

    # obtain dictionary, corpus from document list
    texts = [text.split() for text in prep_list]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # define LSI-space
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=num_topics)

    # prepare query
    preprocessed = preprocess(query)
    query_bow = dictionary.doc2bow(preprocessed)
    query_lsi = lsi[query_bow]

    # apply lsi model to whole corpus and index
    index = similarities.MatrixSimilarity(lsi[corpus])

    # apply similarity measure, sort and extract indices
    sims = index[query_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    indices, x = zip(*sims)

    # obtain first num_doc list entries
    return indices[:num_docs]

def getStringSimilarityDegree(str1, str2):
    '''
    Retrieves the similarity degree of two string
    :param:
    str1: first string input (string)
    str2: second string input (string)
    :return: similarity: similarity degree of two strings (float)
	'''

    similarity =  SequenceMatcher(None, str1, str2).ratio()
    return similarity
