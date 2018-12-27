from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD

def getOccurrenceMatrix(preprocessed_list):
    '''
    Create the occurrence matrix
    :param:
    preprocessed_list: preprocessed documents (list of strings)
    :return: occ_mtx: matrix based occurrence count per document (np array)
    '''
    vectorizer = CountVectorizer()
    occ_mtx = vectorizer.fit_transform(preprocessed_list).toarray()

    return occ_mtx

def feature_selection_variance(occ_mtx, p):
    '''
    Use variance threshold for feature selection
    :param:
    occ_mtx: feature matrix based on occurrence count (np array)
    p: probability threshhold (integer in [0,1])
    :return: selected: occurrence matrix with lesser dimension (np array)
    '''
    sel = VarianceThreshold(threshold=(p * (1 - p)))
    selected = sel.fit_transform(occ_mtx)

    return selected

def get_selected_vocab(selected, occ_mtx, vocabulary):
    '''
    Returns a list of the selected vocabulary after feature selection
    :param:
    selected: occurrence matrix with lesser dimension (np array)
    occ_mtx: original occurrence matrix (np array)
    vocabulary: vocabulary (list)
    :return: selected voc: selected vocabulary (list of strings)
    '''
    found = 0
    selected_voc = []
    for j in range(selected.shape[1]):
        for i in range(found, occ_mtx.shape[1]):

            # compare columns
            if (occ_mtx[:,i] == selected[:,j]).all():
                selected_voc.append(vocabulary[i])
                found = i+1
                break

    return selected_voc

def tf_idf(occ_mtx):
    '''
    Calculated term weight by tf_idf model
    :param: occ_mtx: matrix based on occurrence count (np array)
    :return: tf_idf: matrix of tf_idf values (scipy sparse matrix)
    '''
    transformer = TfidfTransformer(smooth_idf=False)
    return transformer.fit_transform(occ_mtx)

def tf_idf_select(preprocessed_list, min_df):
    '''
    Calculated term weight by tf_idf model, feature selection by df
    :param:
    preprocessed_list: preprocessed documents (list of strings)
    min_df: document frequency threshhold (integer in [0,1])
    :return:
    X: tf_idf matrix with lesser dimension (scipy sparse matrix)
    selected: selected vocabulary (list of strings)
    '''
    vectorizer = TfidfVectorizer(min_df=min_df)
    X = vectorizer.fit_transform(preprocessed_list)

    selected = vectorizer.get_feature_names()

    return X, selected

# TODO!!
def dimensionality_reduction_LSA(tf_idf, n_components):
    '''
    Use LSA for dimensionality reduction
    :param: tf_idf: tf_idf matrix, n_components: desired number of features (int)
    :return: selected: tf_idf matrix with lesser dimension
    '''
    svd = TruncatedSVD(n_components=n_components)

    selected = svd.fit_transform(tf_idf)
    print(svd.explained_variance_ratio_)

    # # lsa results have to be normalized for using k-means
    # normalizer = Normalizer(copy=False)
    # lsa = make_pipeline(svd, normalizer)

    # selected = lsa.fit_transform(tf_idf)

    return selected
