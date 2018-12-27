from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

from read_data import *
from ner_spacy import getArticleInfo

def mergeComponents(i,j, components):
    '''
    Merges two components at given indices in component list
    :param:
    i, j: component indices to merge (integers)
    components: list of componends (list of list of tuples)
    :return:
    new_comp: new component obtained by merging components i, j (list of tuples)
    '''

    comp1 = components[i]
    comp2 = components[j]
    new_comp = comp1.copy() + comp2.copy()
    components.remove(comp1)
    components.remove(comp2)
    return new_comp

def getComponents(linked):
    '''
    Obtains connected components of interdependent events
    :param:
    linked: indeces of articles that are linked (list of tuples)
    :return:
    components: connected components (list of list of tuples)
    '''

    components = []

    for x,y in linked:
        flattened = [[e for tup in comp for e in tup] for comp in components]
        same = 0

        # both indices are in the same component already
        for comp in flattened:
            if x in comp and y in comp:
                same = 1
                break
        if same == 1:
            continue               

        # both indices are in different components
        for i in range(len(flattened)):
            for j in range(len(flattened)):
                if x in flattened[i] and y in flattened[j]:
                    new_comp = mergeComponents(i,j, components)
                    new_comp.append((x,y))
                    same = 1
                    break
        if same == 1:
            continue

        # only one of the tuples appears
        for i in range(len(flattened)):
            if x in flattened[i] or y in flattened[i]:
                components[i].append((x,y))
                same = 1
                break
        if same == 1:
            continue

        components.append([(x,y)])

    return components

def get_independent(linked, similar_events):
    '''
    Obtains the idices of parameters that are indipendent
    :param:
    linked: indeces of articles that are linked (list of tuples)
    similar_events: idices of events that are similar to the issue description (list)
    :return:
    independent: independent components (list of tuples of one element)
    '''

    # flatten linked, obtain list of indices
    dependent = [x for tup in linked for x in tup]
    independent = []

    # append all non-dependent events as components
    for x in similar_events:
        if x not in dependent:
            independent.append([(x,)])

    return independent

def visualizeInterDependency(linked, dataset, similar_events, issue_descr):
    '''
    Vizualizes the interdependency of dependent and interdependent articles in html file
    :param:
    linked: indeces of articles that are linked (list of tuples)
    dataset (table)
    similar_events: idices of events that are similar to the issue description (list)
`   issue descr: description of an issue from description.txt (string)
    :return:
    None
    '''

    # format issue description
    title = issue_descr.partition("]")[2][0:50]+"..."

    # obtain dependent and independent components
    linked_comp = getComponents(linked)
    indep_comp = get_independent(linked, similar_events)

    # concatenate all components
    components = linked_comp + indep_comp

    edge_traces = []
    node_traces = []
    offset = 0

    for j in range(len(components)):
        comp = components[j]

        # obtain chronologically sorted index list of all articles
        index_list = list(set([x for tup in comp for x in tup]))
        index_list.sort()

        # obtain article information
        dates = getArticleDatesByIndex(index_list, dataset)
        titles = getArticleHeadingsByIndex(index_list, dataset)
        articles = getArticleBodyByIndex(index_list, dataset)
        descriptions = getArticleDescriptionsByIndex(index_list, dataset)

        # convert pandas timestamp to unix time
        unix_dates = [t.value // 10 ** 9 for t in dates]

        # create edge list for each component
        edge_traces.append(go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5,color='#888'),
            hoverinfo='none',
            mode='lines'))

        # create node list for each component
        node_traces.append(go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            marker=dict(
                size=10
                ),
            hoverinfo='text'))

        for i in range(len(index_list)):

            # format article information
            people, organizations, places, _ = getArticleInfo(articles[i])
            people = str(people.keys()).replace("dict_keys([", "").replace("])", "")
            organizations = str(organizations.keys()).replace("dict_keys([", "").replace("])", "")
            places = str(places.keys()).replace("dict_keys([", "").replace("])", "")
            description = titles[i]+"<br>People: "+str(people)+"<br>Organizations: "+str(organizations)+"<br>Places: "+str(places)+"<br>Date: "+str(dates[i])[0:10]

            # append artice to node and edge list of component
            node_traces[j]["y"] += tuple([5+offset])
            node_traces[j]["x"] += tuple([unix_dates[i]])
            edge_traces[j]["y"] += tuple([5+offset])
            edge_traces[j]["x"] += tuple([unix_dates[i]])
            node_traces[j]['text']+=tuple([description])

        # add component offset
        offset += 10

    data = edge_traces + node_traces

    # create figure
    fig = go.Figure(data=data,
                 layout=go.Layout(
                    title=title,
                    titlefont=dict(size=40),
                    showlegend=False,
                    hovermode='closest',
                    yaxis=dict(showgrid=False, showticklabels=False),
                    xaxis=dict(
                        title='TIME',
                        titlefont=dict(
                            color='lightgrey',
                            size=20
                            ),
                        tickfont=dict(
                            size=15),
                        tickvals=[1420070400, 1451606400, 1483228800, 1514764800],
                        ticktext=['2015', '2016', '2017', '2018'],
                        showticklabels=True,
                    )
    ))
    
    # plot figure (will open html file in browser)
    plot ( fig )
