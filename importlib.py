#Code to read a gml file and output the dot file conserving edge colors and arrowhead type

import networkx as nx
import pydot


def gml2dot(fname):
    
    print 'Importing graph from', fname,'...'
    
    #Import graph from gml file
    G = nx.DiGraph()
    G = nx.read_gml(fname)
    
    edge_list = [[],[],[]]
    
    #Assign node color as readable by dot files and property mapper in yEd.
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
            
    
    #Obtain a list of nodes
    n = G.nodes(data=True)        
    node_list = []    
    for j in n:
        node_list.append(j[0])
    
    #Create a new graph to save only the required properties (yEd saves a lot of other details we do not want like orientation, position, etc.)
    H = nx.DiGraph()
    
    #Add all nodes with the labels in the new graph
    for k in node_list:
        H.add_node(k)
        H.node[k]['label'] = k
    
    #Add all the edges with color and arrow type in the new graph
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
    print 'Done.'
    return H