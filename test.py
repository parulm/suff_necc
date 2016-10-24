import importlib
import networkx as nx

import gprops
import subgraph
import nodeprops
import reduction

fname = '/home/parul/codes/test_networks/LGL_new_red3_1.gml'
#fname = '/home/parul/codes/test_networks/source_status/LGL_new_red3_stimuliOFF1.gml'
G = nx.DiGraph()

G = importlib.gml2dot(fname)

gprops.set_edge_type(G)
'''
gprops.set_node_type(G)

gprops.lone_reg(G)
reduction.homog_node(G)
reduction.node_collapse(G)

gprops.set_edge_props(G)
'''
nodelist = [[],[],[]]
nodelist[0] = G.nodes()
l = len(nodelist[0])
for i in range(l):
	nodelist[1].append(0)
	nodelist[2].append('null')

print subgraph.find_sg_allpath(G,'Stimuli','Apoptosis')
'''
for source in G.nodes():
	print 'Scanning',source
	sg = subgraph.find_sg_by_path(G,source,source)
	if sg is not None:
		print source,sg


#print subgraph.find_sg_allpath(G,'Ceramide','Apoptosis')


#PDGF_list = ['10','4','25','21','TRADD','3','7','8','FasL','PI3K','PDGFR','IFNGT','19','NFKB']
#PDGF_list = ['TPL2']
#PDGF_list = ['TCR','1','13']
#PDGF_list = ['GAP','9','SOCS']
PDGF_list = ['TCR']
for source in PDGF_list:
	print 'Source node as:',source
	nodeprops.set_node_allpath(G,source,nodelist)
	print 'Subgraphs now \n'
	nodeprops.set_node_by_sg(G,source,nodelist)
#nodeprops.nodeprp_sg(G,source,'Fas',nodelist)



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

flag=0
for path in nx.all_simple_paths(G,'PDGF','S1P'):
	if len(path)<30:
	#	print 'path no',flag+1,'\t Path',path
	#else:
	#	break
		flag+=1

print flag

ways = nx.all_simple_paths(G,'S1P','S1P')
roads = list(ways)
roadsprime = sorted(roads, lambda x,y: 1 if len(x)>len(y) else -1 if len(x)<len(y) else 0)
for way in roadsprime:
	print len(way)
'''