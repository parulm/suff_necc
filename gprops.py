#Defines the graph properties

import networkx as nx
import pydot
import pygraphviz

import gml2dot


#file_name = '/home/parul/python/graphs_try/t2_2.gml'

def importgraph(file_name):
    G = nx.DiGraph()
    G = gml2dot.gml2dot(file_name)
    return G


def set_edge_type(G):
    for edge in G.edges():
        arr = G.get_edge_data(*edge)
        u = edge[0]
        v = edge[1]
        col = arr['color']
        etype = arr['arrowhead']
        if col=='red':
            if etype=='normal':
                G[u][v]['edge_attr']='s'
            elif etype=='tee':
                G[u][v]['edge_attr']='si'
        elif col=='blue':
            if etype=='normal':
                G[u][v]['edge_attr']='n'
            elif etype=='tee':
                G[u][v]['edge_attr']='ni'
        elif col=='black':
            if etype=='normal':
                G[u][v]['edge_attr']='s/n'
            elif etype=='tee':
                G[u][v]['edge_attr']='s/ni'
                
    return G


'''
H = nx.DiGraph()
H = importgraph(file_name)
H = set_edge_type(H)
print H.node
print H.edge
'''