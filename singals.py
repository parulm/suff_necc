import networkx as nx
import importlib
import gprops

fname = '/home/parul/Dropbox/codes/rules/EMT_complt/main.txt'

G = importlib.read_boolean(fname)
gprops.set_edge_type(G)
gprops.set_node_type(G)


signals = ['SHH','Wnt','HGF','PDGF','IGF1','EGF','FGF','Jagged','TGFb','DELTA','CHD1L','Goosecoid','Hypoxia']

for node in signals:
	gprops.update_graph(G,node,'OFF')
	
outfname = '/home/parul/Dropbox/codes/EMT_complt/signalsOFF.graphml'
nx.write_graphml(G,outfname)