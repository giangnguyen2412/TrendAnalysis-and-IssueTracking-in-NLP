import collections
import pandas
import numpy
from sklearn.cluster import KMeans

def computeTopTen(cluster_prediction, testing):
    '''
    Picks the top ten clusters (most articles in their cluster) that have less than 150 articles,
    sorted from most articles to least out of the kMeans.predict() result
    :param:
    cluster_prediction (array of integer): the result of the predict function of the kMeans algorithm
    testing (bool): wether the clustering gets tested or not
    :return: the top ten clusters sorted after the number of articles in each cluster,
    type: list of tuples(x, y) of integers
    '''

    counts = collections.Counter(cluster_prediction)
    countsFiltered = list(filter(lambda x: (x[1] < 150), counts.most_common()))

    if testing:
        print("clusters sorted after their number of articles:", counts,most_common(10), "\n")

    return countsFiltered[:10]

def evaluateClusterParameter(file, cluster, headings):
    '''
    Prints out the result of the clustering - the titles belonging to each cluster and
    the sum of squared distances of the articles to their closest cluster center
    :param:
    cluster (array like): the result of the clustering
    headings (array of sets): the titles of the articles belonging to the i-th cluster
    :return: nothing
    '''

    print("sum of squared distances to the cluster centers:", cluster.inertia_, "\n")
    file.write("sum of squared distances to the cluster centers:")
    file.write(str(cluster.inertia_))
    file.write("\n")

    for i in range(len(headings)):
        print("headings for cluster", i, ":", headings[i])
        file.write("headings for cluster ")
        file.write(str(i))
        file.write(":")
        file.write(str(headings[i]))
        file.write("\n")

    print("\n")

def getArticleHeadings(cluster_prediction, number_clusters, dataset):
    '''
    Sortes the titles of the articles to the clusters in which the articles belong
    :param:
    cluster_prediction (array of integer): the result of the predict function of the kMeans algorithm
    number_custers (integer): the number of clusters which were created
    dataset (table): the raw data which was the foundation of preprocessing, term weighting and clustering
    :return: the titles of articles grouped into the cluster in which the articles belong,
    type: array of sets of strings
    '''

    cluster_headings = [set() for _ in range(number_clusters)]

    for i in range(len(cluster_prediction)):
        cluster_headings[cluster_prediction[i]].add(dataset.ix[i]['title'])

    return cluster_headings

def getTopTenHeadings(cluster_headings, top_ten):
    '''
    Reduces the sets of titles of the clusters to the top ten clusters
    :param:
    cluster_headings (array of sets of strings): the titles matched to the clusters
    top_ten (array of tuples(x, y) of integers): the sorted indices of the top ten clusters
    :return: the titles belonging to the top ten clusters matched to their cluster,
    type: array of sets of strings
    '''

    headings = [set() for _ in range(10)]

    for i in range(10):
        headings[i] = cluster_headings[((top_ten[i])[0])]

    return headings

def getTopTenVocabulary(cluster_vocabulary, top_ten):
    '''
    Reduces the sets of terms of the clusters to the top ten clusters
    :param:
    cluster_vocabulary (array of sets of strings): the terms matched to their clusters
    top_ten (array of tuples(x, y) of integers): the sorted indices of the top ten clusters
    :return: the terms belonging to the top ten clusters matched to their clusterm,
    type: array of sets of strings
    '''

    vocabulary = [set() for _ in range(10)]

    for i in range(10):
        vocabulary[i] = cluster_vocabulary[((top_ten[i])[0])]

    return vocabulary

def getVocabularyOfClusters(cluster_prediction, number_clusters, tf_idf_matrix, selected_voc):
    '''
    Sortes the terms of the articles to the clusters in which the articles belong
    :param:
    cluster_prediction (array of integer): the result of the predict function of the kMeans algorithm
    number_custers (integer): the number of clusters which were created
    tf_idf_matrix (sparse matrix of floats): the term-document matrix, result of the term weighting
    slected_voc (array of strings): the terms which are the foundation of the tf-idf matrix, result of the term weighting
    :return: the terms of the articles grouped into the cluster in which the articles belong,
    type: array of sets of strings
    '''

    cluster_vocabulary = [set() for _ in range(number_clusters)]

    for i in range(len(cluster_prediction)):
        article_vocabulary = set()

        for j in range(len(numpy.nonzero(tf_idf_matrix[i,:])[1])):
            article_vocabulary.add(selected_voc[((numpy.nonzero(tf_idf_matrix[i,:])[1])[j])])

        cluster_vocabulary[cluster_prediction[i]] = cluster_vocabulary[cluster_prediction[i]].union(article_vocabulary)

    return cluster_vocabulary

def kMeansClustering(num_clusters, tf_idf_matrix, max_iterations, selected_voc, dataset, testing):
    '''
    The main function of clustering, controlls the clustering flow
    :param:
    num_clusters (integer): the number of clusters to be created
    tf_idf_matrix (sparse matrix of floats): the term-document matrix, result of the term weighting
    max_iterations (integer): the maximum number of iterations the k-means algorithm can make
    -> more iterations, the longer it takes to compute but the results are normaly better
    selected_voc (array of strings): the terms which are the foundation of the tf-idf matrix, result of the term weighting
    dataset (table): the raw data which was the foundation of preprocessing, term weighting and clustering
    testing (bool): wether the clustering gets tested or not
    :return: the indices of the top ten clusters, sorted after the number of articles in them,
    the titles of the top ten clusters and the terms of the top ten clusters,
    type: array of tuples(x, y) of integers, array of sets of strings, array of sets of strings
    '''

    if testing:
        testKMeansClustering(tf_idf_matrix, max_iterations, dataset)

    cluster = performClustering(num_clusters, tf_idf_matrix, max_iterations)
    cluster_prediction = predictCluster(cluster, tf_idf_matrix)
    top_ten = computeTopTen(cluster_prediction, False)
    cluster_vocabulary = getVocabularyOfClusters(cluster_prediction, num_clusters, tf_idf_matrix, selected_voc)
    cluster_headings = getArticleHeadings(cluster_prediction, num_clusters, dataset)
    top_ten_vocabulary = getTopTenVocabulary(cluster_vocabulary, top_ten)
    top_ten_headings = getTopTenHeadings(cluster_headings, top_ten)

    return top_ten, top_ten_headings, top_ten_vocabulary

def performClustering(num_clusters, tf_idf_matrix, max_iterations):
    '''
    Performs the k-means clustering algorithm
    :param:
    num_clusters (integer): the number of clusters to be created
    tf_idf_matrix (sparse matrix of floats): the term-document matrix, result of the term weighting
    max_iterations (integer): the maximum number of iterations the k-means algorithm can make
    -> more iterations, the longer it takes to compute but the results are normaly better
    :return: the result of the k-means clustering,
    type: array like
    '''

    return KMeans(n_clusters=num_clusters, init='k-means++', max_iter=max_iterations, n_init=10).fit(tf_idf_matrix)

def predictCluster(cluster, tf_idf_matrix):
    '''
    Retrieves the result of the clustering, the indicies of the cluster each article belongs to
    :param:
    cluster (array like): the result of the k-means clustering algorithm
    tf_idf_matrix (sparse matrix of floats): the term-document matrix, result of the term weighting
    :return: the indices of the clusters each article belongs to,
    type: array of integers
    '''

    return cluster.predict(tf_idf_matrix)

def printTopTen(to_print):
    '''
    Prints either the titles or terms of the top ten clusters
    :param:
    to_print (array): either the titles or terms of the top ten clusters to be visualized on the screen
    :return: nothing
    '''

    for i in range(10):
        print(i, ":", to_print[i])

    print("\n")

def printTopTenToFile(file, headings, vocabulary):
    '''
    Writes the headings and vocabulary of the top ten clusters to file
    :param:
    file (file descriptor): the file describtor in which file should be written
    headings (array): the headings of the top ten clusters
    vocabulary (array): the vocabulary of the top ten clusters
    :return: nothing
    '''

    for i in range(10):
        try:
            file.write("cluster ")
            file.write(str(i))
            file.write("\n- Length:")
            file.write(str(len(headings[i])))
            file.write("\n- headings: ")
            file.write(str(headings[i]))
            file.write("\n- vocabulary: ")
            file.write(str(vocabulary[i]))
            file.write("\n\n\n")
        except:
            file.write("exception occured\n\n\n")

def testKMeansClustering(tf_idf_matrix, max_iterations, dataset):
    '''
    Tests in a loop the best parameter for k for the k-means clustering and writes the results to the file evaluate.txt
    :param:
    tf_idf_matrix (sparse matrix of floats): the term-document matrix, result of the term weighting
    max_iterations (integer): the maximum number of iterations the k-means algorithm can make -> more iterations,
    the longer it takes to compute but the results are normaly better
    dataset (table): the raw data which was the foundation of preprocessing, term weighting and clustering
    :return: nothing
    '''
    
    file = open("evaluate.txt", "w")

    for i in range(100, 200):
        file.write("k = ")
        file.write(str(i))
        file.write("\n")

        print("number of clusters:", i, "\n")
        
        cluster = performClustering(i, tf_idf_matrix, max_iterations)
        cluster_prediction = predictCluster(cluster, tf_idf_matrix)

        print("cluster - articles matching:", cluster_prediction, "\n")

        cluster_headings = getArticleHeadings(cluster_prediction, i, dataset)
        top_ten = computeTopTen(cluster_prediction, True)

        print("Top 10:", top_ten, "\n")

        top_ten_headings = getTopTenHeadings(cluster_headings, top_ten)
        evaluateClusterParameter(file, cluster, top_ten_headings)

        input("Press enter to continue with the next iteration.")
