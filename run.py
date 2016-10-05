
import networkx as nx

import gml2dot
import gprops
import path
import reduction

#filename = '/home/parul/python/graphs_try/trialf.gml'
filename = '/home/parul/codes/ABA/ABA_s1_red02.gml'


G = gprops.importgraph(filename)
G = gprops.set_edge_type(G)

reduction.lone_reg(G)
reduction.node_red(G)

#outfname = '/home/parul/python/graphs_try/trialf_out.graphml'
outfname = '/home/parul/codes/ABA/ABA_s1_red3.graphml'
nx.write_graphml(G,outfname)