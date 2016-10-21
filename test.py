import importlib
import networkx as nx

import gprops
import subgraph
import nodeprops

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

#nodeprops.nodeprp_path(G,'S1P','Ceramide',nodelist)
#nodeprops.nodeprp_sg(G,'S1P','S1P',nodelist)

#print len(list(nx.simple_cycles(G)))

cycs = list(nx.simple_cycles(G))
flag = 0
for cyc in cycs:
	print cyc
	if flag > 10:
		break
	flag+=1

#way = []

#print subgraph.find_sg(G,'PDGF','Ceramide',nodelist,way)

'''
flag=0
for path in nx.all_simple_paths(G,'PDGF','S1P'):
	if len(path)<30:
	#	print 'path no',flag+1,'\t Path',path
	#else:
	#	break
		flag+=1

print flag
'''
'''
ways = nx.all_simple_paths(G,'S1P','S1P')
roads = list(ways)
roadsprime = sorted(roads, lambda x,y: 1 if len(x)>len(y) else -1 if len(x)<len(y) else 0)
for way in roadsprime:
	print len(way)
'''