#Code to reduce a given sufficient necessary network

import networkx as nx
import pydot
import pygraphviz
import path

def edge_red(G):
    for edge in G.edges():
        u = edge[0]
        v = edge[1]
        arr = G.get_edge_data(*edge)
        uv_type = arr['edge_attr']
        for route in nx.all_simple_paths(G, source=u, target=v):
            if len(route)<=2:
                continue
            if path.path_type(G,route)==uv_type:
                G.remove_edge(u,v)
                break
            else:
                continue
    
    return None


def node_red(G):
    for node in G.nodes():
        s_list = G.successors(node)
        p_list = G.predecessors(node)
        if len(s_list)==1 and len(p_list)==1:
            parent = p_list[0]
            child = s_list[0]
            parent_relationship = G[parent][node]['edge_attr']
            child_relationship = G[node][child]['edge_attr']
            if parent_relationship==child_relationship:
                G.remove_node(node)
        
    return G

def lone_reg(G):
    for node in G.nodes():
        regs = G.predecessors(node)
        if len(regs)==1:
            parent = regs[0]
            G[parent][node]['edge_attr']='s/n'
            
    return G