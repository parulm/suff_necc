import networkx as nx

import importlib
import nodeprops
import gprops
import subgraph
import reduction

#fname = '/home/parul/codes/test_networks/LGL_subset.gml'
fname = '/home/parul/codes/test_networks/EMT.txt'
G = nx.DiGraph()

#G = importlib.gml2dot(fname)
G = importlib.read_boolean(fname)

gprops.set_edge_type(G)
gprops.set_node_type(G)
'''
reduction.edge_red(G)
gprops.lone_reg(G)
reduction.node_red(G)
gprops.lone_reg(G)
reduction.node_collapse(G)
gprops.lone_reg(G)
reduction.edge_red(G)
gprops.lone_reg(G)
reduction.homog_node(G)
gprops.lone_reg(G)
reduction.node_collapse(G)
gprops.lone_reg(G)
reduction.edge_red(G)
gprops.lone_reg(G)
reduction.homog_node(G)
gprops.lone_reg(G)
'''
gprops.set_edge_props(G)


for source in G.nodes():
	#print 'Scanning',source
	sg = subgraph.find_sg_allpath(G,source,source)
	if sg is not None:
		print source,sg


#sources = []
#motifs = ['GLI','beta_catenin_membrane','E-cadherin','MEK','AXIN2','GSK3beta','beta_catenin_nuc','SMAD','SNAI1','SNAI2','Dest_compl','ZEB1']
#outfname = '/home/parul/codes/test_networks/EMT/reduced.graphml'
#nx.write_graphml(G,outfname)



'''
nodelist = [[],[],[]]
nodelist[0] = G.nodes()
l = len(nodelist[0])
for i in range(l):
	nodelist[1].append(0)
	nodelist[2].append('null')

#motif = []
#source = 'S1P'
#for source in G.nodes():
#	print source,'motif of type',subgraph.find_sg_by_path(G,source,source)

gnodes = ['FasT','PLCG1','FasL']
for source in gnodes:
	print 'Source node as:',source
	nodeprops.set_node_by_path(G,source,nodelist)
	print 'Subgraphs now \n'
	nodeprops.set_node_by_sg(G,source,nodelist)
'''