import networkx as nx

import importlib
import nodeprops
import gprops

#fname = '/home/parul/codes/test_networks/LGL_subset.gml'
fname = '/home/parul/codes/test_networks/LGL_new.txt'
G = nx.DiGraph()

#G = importlib.gml2dot(fname)
G = importlib.read_boolean(fname)

gprops.set_edge_type(G)

nodelist = [[],[],[]]
nodelist[0] = G.nodes()
l = len(nodelist[0])
for i in range(l):
	nodelist[1].append(0)
	nodelist[2].append('null')

source = 'IL15'
print 'Source node as:',source
nodeprops.set_node_by_path(G,source,nodelist)
print 'Subgraphs now \n'
nodeprops.set_node_by_sg(G,source,nodelist)