from openie_ollie import *
from similarity import *
from read_data import *

relations = ["plan", "plans", "planned" , "calls", "call", "called", "urge", "urges", "urged", "allow", "allows", "allowed"]


def filterPlan(triples):
    '''
    Filter tuples that contain "plan to
    :param:
    triples: input triples to be processed (list)
    :return:
    plan_triples: triples that contain "plan to"
    '''

    plan_triples = []

    for triple in triples:
        for term in triple:
            for relation in relations:

                #check if terms contain relations
                if relation in term:
                    plan_triples.append(triple)

    return plan_triples

def concatenatePlan(triple):
    '''
    Concatenate triple to form a similarity query
    :param:
    triple: entities with relation "plan to" or "plans to" (tuple)
    :return:
    query: concatenated string without "plan to" or "plans to" (string)
    '''

    query = ""

    for term in triple:
        for relation in relations:
            if relation in term:
                query = query+" "+term.replace(relation, "")
            if "enabler" in term:
                continue
            else:
                query = query+" "+term

    return query

def getConfirmation(index, similar_idx, data):
    '''
    Confirm with user if articles are linked, this function for testing, not running
    :param:
    data: input dataset (dataframe)
    index: index of current article (int)
    similar_idx: index of similar article (int)
    :return:
    confirmation: returns 1 if articles are linked, 0 otherwise
    '''

    print(getArticleHeadingsByIndex([index], data)[0], getArticleDatesByIndex([index], data)[0])
    print(getArticleDescriptionsByIndex([index], data)[0], "\n")

    print(getArticleHeadingsByIndex([similar_idx], data)[0], getArticleDatesByIndex([similar_idx], data)[0])
    print(getArticleDescriptionsByIndex([similar_idx], data)[0])
    intent = input('Are these two articles linked? Y/N? ')
    print("\n")

    if (intent in YES_STR_LIST):
        return 1
    return 0


def getInterdependent(data, indexList, dict_list):
    '''
    Measure interdependency of articles of one topic
    :param:
    data: input dataset (dataframe)
    index_list: indices of articles related to one topic (list)
    topic_idx: index of the topic
    :return:
    linked: interdependent article tuples (list of tuples)
    '''

    linked = []

    # sort by index for chronological order
    sort = sorted(indexList)

    # get string list for similarity query (without first element)
    article_list = getArticleBodyByIndex(sort, data)

    for index in sort:
        # remove current article from article list
        article_list.pop(0)

        # indices are missing if there is no enabler tuple
        if index not in dict_list.keys():
            print("index "+str(index)+" not in dict_list")
            continue

        # obtain triples that contain keywords
        triples = dict_list[index]
        plan_triples = filterPlan(triples)

        for triple in plan_triples:

            # perform similarity query
            query = concatenatePlan(triple)
            similar = getSimilarDocuments(article_list, query, len(article_list), 1)

            # obtain index in sorted list
            similar_idx = sort[similar[0]+sort.index(index)+1]

            # human input to confirm inter-dependency
            # if(getConfirmation(index, similar_idx, data) == 1):
            linked.append((index, similar_idx))

    # remove duplicattions
    return list(set(linked))
