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
gprops.set_node_type(G)

gprops.update_graph(G,'IL15','ON')
gprops.update_graph(G,'PDGF','OFF')

gprops.remove_stray(G)

reduction.node_collapse(G)
reduction.homog_node(G)
reduction.edge_red(G)
reduction.homog_node(G)
reduction.edge_red(G)
gprops.set_edge_props(G)
gprops.lone_reg(G)
reduction.node_collapse(G)
gprops.lone_reg(G)
reduction.homog_node(G)

gprops.set_edge_props(G)


#outf = '/home/parul/codes/test_networks/source_status/bycode/reduced/LGL_new_red3_1_il15ON.graphml'
#nx.write_graphml(G,outf)

'''
gprops.set_node_type(G)

gprops.lone_reg(G)
reduction.homog_node(G)
reduction.node_collapse(G)

gprops.set_edge_props(G)

nodelist = [[],[],[]]
nodelist[0] = G.nodes()
l = len(nodelist[0])
for i in range(l):
	nodelist[1].append(0)
	nodelist[2].append('null')


G.remove_edge('Ceramide','S1P')

gprops.update_graph(G,'S1P','ON')
gprops.lone_reg(G)

gprops.remove_stray(G)
gprops.set_edge_props(G)

reduction.homog_node(G)
reduction.edge_red(G)
reduction.homog_node(G)
gprops.set_edge_props(G)
gprops.lone_reg(G)
reduction.node_collapse(G)

gprops.set_edge_props(G)

G.remove_edge('TBET','IFNG')
gprops.update_graph(G,'IFNG','ON')

gprops.lone_reg(G)

gprops.remove_stray(G)


reduction.homog_node(G)
reduction.edge_red(G)
#gprops.set_edge_props(G)
#reduction.homog_node(G)
#reduction.node_collapse(G)

gprops.set_edge_props(G)
'''
G.remove_edge('IL2RB','RAS')
gprops.update_graph(G,'RAS','ON')

gprops.lone_reg(G)

gprops.remove_stray(G)


reduction.homog_node(G)
reduction.edge_red(G)
reduction.homog_node(G)
gprops.lone_reg(G)


gprops.set_edge_props(G)

G.remove_edge('Ceramide','S1P')

gprops.update_graph(G,'S1P','ON')
gprops.lone_reg(G)

gprops.remove_stray(G)
gprops.set_edge_props(G)

#print subgraph.find_sg_allpath(G,'IL2RB','IL2RB')

'''
for source in G.nodes():
	print 'Scanning',source
	sg = subgraph.find_sg_allpath(G,source,source)
	if sg is not None:
		print source,sg
'''

outfnew = '/home/parul/codes/test_networks/source_status/bycode/reduced/temp.graphml'
nx.write_graphml(G,outfnew)

'''
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