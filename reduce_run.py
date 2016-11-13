
import networkx as nx
import pygraphviz

import importlib
import gprops
import path
import reduction

#filename = '/home/parul/python/graphs_try/trialf.gml'
filename = '/home/parul/codes/ABA/ABA_22.gml'

G = gprops.importgraph(filename)
G = gprops.set_edge_type(G)

n=4
print 'Running edge reduction and node reduction sequentially ',n,' times.'
for i in range(n):
    reduction.edge_red(G)
    gprops.set_edge_props(G)
    gprops.lone_reg(G)
    reduction.node_red(G)
    gprops.set_edge_props(G)
    gprops.lone_reg(G)
    reduction.pnode_collapse(G)
    print 'Done with run number ',i+1,'\n'

reduction.homog_pnode(G)

gprops.set_edge_props(G)

k=1
print 'Running edge reduction and node reduction sequentially ',k,' times.'
for i in range(k):
    reduction.edge_red(G)
    gprops.set_edge_props(G)
    gprops.lone_reg(G)
    reduction.node_red(G)
    gprops.set_edge_props(G)
    gprops.lone_reg(G)
    reduction.pnode_collapse(G)
    print 'Done with run number ',i+1,'\n'

print 'Doing homogenous reduction again'
reduction.homog_pnode(G)

gprops.set_edge_props(G)

'''
#outfname = '/home/parul/python/graphs_try/trialf_out.graphml'
outfname = '/home/parul/codes/ABA/ABA_11.graphml'
nx.write_graphml(G,outfname)
'''