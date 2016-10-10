#Defines the graph properties

import networkx as nx
import pydot
import pygraphviz

import gml2dot


def importgraph(file_name):
    G = nx.DiGraph()
    G = gml2dot.gml2dot(file_name)
    return G


def set_edge_type(G):
    print 'Setting edge attribute from color and arrow types ...'
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
    print 'Done.'            
    return G


def test_homog(G):
    for node in G.nodes():
        regulators = G.predecessors(node)
        old_type = G[regulators[0]][node]['edge_attr']
        for r in regulators:
            new_type = G[r][node]['edge_attr']
            if new_type!=old_type:
                if new_type=='s' and old_type=='ni':
                    continue
                elif new_type=='ni' and old_type=='s':
                    continue
                elif new_type=='n' and old_type=='si':
                    continue
                elif new_type=='si' and old_type=='n':
                    continue
                else:
                    print 'Homogeneity is not being followed at node ',node
                    break
                
    return None


def node_homog(G,node):
    regulators = G.predecessors(node)
    old_type = G[regulators[0]][node]['edge_attr']
    for r in regulators:
        new_type = G[r][node]['edge_attr']
        if new_type!=old_type:
            if new_type=='s' and old_type=='ni':
                continue
            elif new_type=='ni' and old_type=='s':
                continue
            elif new_type=='n' and old_type=='si':
                continue
            elif new_type=='si' and old_type=='n':
                continue
            else:
                return False
        #old_type = new_type
    return True


def set_edge_props(G):
    print 'Setting graphic properties of edges ...'
    for node in G.nodes():
        regulators = G.predecessors(node)
        for r in regulators:
            etype = G[r][node]['edge_attr']
            if etype=='s':
                G[r][node]['color']='red'
                G[r][node]['arrowhead']='normal'
            elif etype=='si':
                G[r][node]['color']='red'
                G[r][node]['arrowhead']='tee'
            elif etype=='n':
                G[r][node]['color']='blue'
                G[r][node]['arrowhead']='normal'
            elif etype=='ni':
                G[r][node]['color']='blue'
                G[r][node]['arrowhead']='tee'
            elif etype=='s/n':
                G[r][node]['color']='black'
                G[r][node]['arrowhead']='normal'
            elif etype=='s/ni':
                G[r][node]['color']='black'
                G[r][node]['arrowhead']='tee'
    print 'Done.'
    return None


def set_node_type(G):
    print 'Setting node types for all nodes'
    print 'This function must be run after testing for Homogeneity!'
    for node in G.nodes():
        regulator = G.predecessors(node)[0]
        ntype = G[regulator][node]['edge_attr']
        if ntype=='s' or ntype=='ni':
            node_color = 'red'
        elif ntype=='n' or ntype=='si':
            node_color = 'blue'
        elif ntype=='s/n' or ntype=='s/ni':
            node_color = 'black'
        
        G.node[node]['ncolor']=node_color
    print 'Done.'
    return None


def node_type(G,node):
    regulator = G.predecessors(node)[0]
    ntype = G[regulator][node]['edge_attr']
    if ntype=='s' or ntype=='ni':
        node_color = 'red'
    elif ntype=='n' or ntype=='si':
        node_color = 'blue'
    elif ntype=='s/n' or ntype=='s/ni':
        node_color = 'black'
    return node_color


def lone_reg(G):
    print 'Setting all single regulator nodes as suff/necc or inhibitory suff/necc ...'
    for node in G.nodes():
        regs = G.predecessors(node)
        if len(regs)==1:
            parent = regs[0]
            if G[parent][node]['edge_attr']=='s/n' or G[parent][node]['edge_attr']=='s/ni':
                break
            if G[parent][node]['arrowhead']=='normal':
                newt = 's/n'
            elif G[parent][node]['arrowhead']=='tee':
                newt = 's/ni'
            print 'Setting edge',parent,'->',node, 'as',newt
            G[parent][node]['edge_attr']=newt
            
    print 'Done'
    return G

