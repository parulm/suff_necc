import networkx as nx

import importlib
import subgraph
import gprops
import path

fname = '/home/parul/codes/test_networks/LGL_new.txt'
G = nx.DiGraph()
G = importlib.read_boolean(fname)
gprops.set_edge_type(G)

nodelist = [[],[],[]]
nodelist[0] = G.nodes()
l = len(nodelist[0])
for i in range(l):
	nodelist[1].append(0)
	nodelist[2].append('null')

sources = ['IL15','Stimuli','PDGF']
motif_nodes = ['TBET','Ceramide','S1P','PDGFR','SPHK1']
output = ['Apoptosis']

for source in sources:
	for onode in motif_nodes:
		inode = source
		found=0
		for route in nx.all_simple_paths(G,source,onode):
			if path.path_type(G,route) is not 'nothing':
				print path.path_type(G,route)
				found = 1
		if found==0:
			nodelist = [[],[],[]]
			nodelist[0] = G.nodes()
			l = len(nodelist[0])
			for i in range(l):
				nodelist[1].append(0)
				nodelist[2].append('null')
			print inode,'->',onode,'of type',subgraph.find_subgraph(G,inode,onode,source,'s/n',nodelist)
			

'''
nodes = G.nodes()
for source in nodes:
	for onode in nodes:
		#if source==onode:
		#	continue
		inode = source
		found = 0
		for route in nx.all_simple_paths(G,source,onode):
			if path.path_type(G,route) is not 'nothing':
				print source,'->',onode,'of type:',path.path_type(G,route)
				found = 1
		if found==0:
			nodelist = [[],[],[]]
			nodelist[0] = G.nodes()
			l = len(nodelist[0])
			for i in range(l):
				nodelist[1].append(0)
				nodelist[2].append('null')
			stype = subgraph.find_subgraph(G,inode,onode,source,'s/n',nodelist)
			print inode,'->',onode,'of type:',stype
'''