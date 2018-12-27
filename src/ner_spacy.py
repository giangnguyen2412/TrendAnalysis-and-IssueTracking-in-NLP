'''
Created on Nov 15, 2018

@author: Giang Nguyen
@email: dexter.nguyen7@kaist.ac.kr

'''

from global_definition import *

def extractNERSpacy(inputDataFrame, indexList):
    '''
    Extract Name Entity using Spacy NER
    :param: indexList: A list of two lists corresponding two topics.
    Each list includes indices of articles in dataframe (list)
    :param: inputDataFrame: Dataframe from raw dataset (dataframe)
    :return: NER_list: A list of two dictionaries corresponding to two topics.
    Each dictionary includes keys are indices of articles in dataframe, data is
    a set of entities of with an index in dataframe (list)
    '''

    # A list of dictionaries
    dictionary_list = [dict(), dict()]

    topic_num = len(indexList)

    # Over topics
    for topic_idx in range(topic_num):
        # Over all articles of a topic
        for df_idx in (indexList[topic_idx]):
            # Get the entry(article) in dataframe
            article = inputDataFrame.ix[df_idx]
            # Get body of an articles
            art_body = article[BODY_STR]
            # Construct a spacy doc object
            spacy_doc = spc(art_body)
            # Get name entities
            entity_tup = spacy_doc.ents
            entity_set = set(entity_tup)

            for entity in entity_set.copy():
                # Filter entities
                if entity.label_ not in ENTITY_TYPE:
                    entity_set.remove(entity)
            dictionary_list[topic_idx][df_idx] = entity_set

    NER_list = dictionary_list
    return NER_list

def articleNER(article):
    '''
    Extract NER list for an article string
    :param: article : Body string of an article(string)
    :retrun: entities, duplicates may occur because we use (list)
    '''
    # Construct a spacy doc object
    spacy_doc = spc(article)
    # Get name entities
    entities = set(spacy_doc.ents)

    for entity in entities.copy():
        # Filter entities
        if entity.label_ not in ENTITY_TYPE:
            entities.remove(entity)

    return list(entities)


def addToDict(dictionary, term):
    '''
    Add a key to the dictionary to obtain the occurrence count
    :param:
    dictionary: a dictionary (person name dict, org dict ...) (dict)
    term: term to be add to dictionary (string)
    :return:
    None
    '''

    if str(term) not in dictionary:
        dictionary[str(term)] = 1
    else:
        dictionary[str(term)] += 1

def getArticleInfo(article):
    '''
    Extract NER list for an article string
    :param:
    article: Body string of an article (string)
    :return:
    people: person name dictionary (dict)
    organizations: organization name dictionary (dict)
    places: location name dictionary (dict)
    dates: time dictionary (dict)
    '''

    # get the named entities
    NER_list = articleNER(article)

    people = {}
    organizations = {}
    places = {}
    dates = {}

    for term in NER_list:

        # Wrong text format
        if '."' in term.text or '(' in term.text or ')' in term.text or '\'s' in term.text or 'H5' in term.text:
            continue

        if term.text == 'Zika':
                continue

        if term.text == 'Park':
            addToDict(people, term)
            continue

        if term.text == 'Yonhap':
            addToDict(organizations, term)
            continue

        if term.label_ == "ORG":
            addToDict(organizations, term)

        if term.label_ == "DATE":
            addToDict(dates, term)

        if term.label_ == "GPE":
            if (term.text[0].isupper() == False):
                continue
            addToDict(places, term)

        if term.label_ == "PERSON":
            if (term.text[0].isupper() == False):
                continue
            if ((len(term.text.split()) == 1) and ('-' not in term.text)):
                continue
            addToDict(people, term)

    return people, organizations, places, dates
