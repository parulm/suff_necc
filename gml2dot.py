#Code to read a gml file and output the dot file conserving edge colors and arrowhead type

import networkx as nx
import pydot
#import sys

#gmlfile = sys.argv[1]

#gmlfile = 'test.gml'

def gml2dot(fname):
    
    #fname = gmlfile + '.gml'
    
    G = nx.DiGraph()
    G = nx.read_gml(fname)
    
    edge_list = [[],[],[]]
    l = G.edges()
    for i in l:
        m = G.get_edge_data(*i)
        if m[u'graphics'][u'fill']=='#0000FF':
            edge_color = 'blue'
        elif m[u'graphics'][u'fill']=='#FF0000':
            edge_color = 'red'
        elif m[u'graphics'][u'fill']=='#000000':
            edge_color = 'black'
            
        if m[u'graphics'][u'targetArrow']=='standard':
            edge_arrow = 'normal'
        elif m[u'graphics'][u'targetArrow']=='t_shape':
            edge_arrow = 'tee'
        
        edge_list[0].append(i)
        edge_list[1].append(edge_color)
        edge_list[2].append(edge_arrow)
            
    n = G.nodes(data=True)        
    node_list = []    
    for j in n:
        node_list.append(j[0])
    
    H = nx.DiGraph()
    
    for k in node_list:
        H.add_node(k)
        H.node[k]['label'] = k
        
    noe = G.number_of_edges()
    for i in range(noe):
        e = edge_list[0][i]
        col = edge_list[1][i]
        etype = edge_list[2][i]
        H.add_edge(*e, color = col, arrowhead = etype)
           
    '''
    dotfname = gmlfile + '.dot'
    nx.drawing.nx_agraph.write_dot(H,dotfname)
    
    graphmlfname = gmlfile + '.graphml'
    nx.write_graphml(H,graphmlfname)
    '''
    return H


#gml2dot(gmlfile)