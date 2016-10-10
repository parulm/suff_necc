#Code to reduce a given sufficient necessary network

import networkx as nx
import pydot
import pygraphviz
import re

import path
import gprops

def edge_red(G):
    print 'Running logical transitive reduction ...'
    for edge in G.edges():
        u = edge[0]
        v = edge[1]
        arr = G.get_edge_data(*edge)
        uv_type = arr['edge_attr']
        for route in nx.all_simple_paths(G, source=u, target=v):
            if len(route)<=2:
                continue
            if path.path_type(G,route)==uv_type:
                print 'Removing edge between',u,'and',v,'by logical transitive reduction'
                G.remove_edge(u,v)
                break
            else:
                continue
    print 'Done.'
    return None


def node_red(G):
    print 'Collapsing nodes with one incoming and one outgoing edge ...'
    for node in G.nodes():
        s_list = G.successors(node)
        p_list = G.predecessors(node)
        if len(s_list)==1 and len(p_list)==1:
            parent = p_list[0]
            child = s_list[0]
            if G.has_edge(parent, child):
                break
            parent_relationship = G[parent][node]['edge_attr']
            child_relationship = G[node][child]['edge_attr']
            if parent_relationship==child_relationship:
                nodename = G.node[node]['label']
                if not re.search('[a-zA-Z]+',nodename):
                    G.add_edge(parent,child,edge_attr=parent_relationship)
                    print 'Removing node',node
                    G.remove_node(node)
    print 'Done.'    
    return G

#add test for feedforward loop in the following function?
def pnode_collapse(G):
    print 'Collapsing pseudo nodes with suff/necc edges ...'
    for node in G.nodes():
        nodename = G.node[node]['label']
        if not re.search('[a-zA-Z]+',nodename):
            s_list = G.successors(node)
            p_list = G.predecessors(node)
            if len(s_list)==1:
                child = s_list[0]
                if G[node][child]['edge_attr']=='s/n':
                    for regulator in p_list:
                        regulator_type = G[regulator][node]['edge_attr']
                        print 'Adding edge',regulator,'->',child,'of type',regulator_type
                        G.add_edge(regulator,child,edge_attr=regulator_type)
                    print 'Removing node',node
                    G.remove_node(node)
            if len(p_list)==1:
                parent = p_list[0]
                if G[parent][node]['edge_attr']=='s/n':
                    for successor in s_list:
                        successor_type = G[node][successor]['edge_attr']
                        print 'Adding edge',parent,'->',successor,'of type',successor_type
                        G.add_edge(parent,successor,edge_attr=successor_type)
                    print 'Removing node',node
                    G.remove_node(node)
    print 'Done'
    return G


def homog_pnode(G):
    print 'Collapsing homogenous pseudo nodes with only one outgoing edge and the type of incoming edges is the same as the outgoing one ...'
    for node in G.nodes():
        nodename = G.node[node]['label']
        if not re.search('[a-zA-Z]+',nodename) and gprops.node_homog(G,node):
            ntype = gprops.node_type(G,node)
            if len(G.successors(node))==1:
                child = G.successors(node)[0]
                etype = G[node][child]['edge_attr']
                flag = False
                if ntype=='red':
                    if etype=='s/n' or etype=='s/ni' or etype=='s' or etype=='si':
                        flag = True
                    else:
                        flag = False
                elif ntype=='blue':
                    if etype=='s/n' or etype=='s/ni' or etype=='n' or etype=='ni':
                        flag = True
                    else:
                        flag = False
                
                if flag:
                    regulators = G.predecessors(node)
                    for r in regulators:
                        rtype = G[r][node]['edge_attr']
                        new_etype = path.add(rtype,etype)
                        if new_etype is not 'null':
                            print 'Adding edge',r,'->',child,'of type',new_etype
                            G.add_edge(r,child,edge_attr=new_etype)
                        else:
                            print 'Critical error in trying to collapse',node
                    print 'Removing node',node
                    G.remove_node(node)
    print 'Done'                
    return None