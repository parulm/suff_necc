import networkx as nx
import importlib
import reduction
import subgraph
import gprops

fname = '/home/parul/Dropbox/codes/rules/EMT_complt/main.txt'

G = importlib.read_boolean(fname)
gprops.set_edge_type(G)
gprops.set_node_type(G)


signals = ['SHH','Wnt','HGF','PDGF','IGF1','EGF','FGF','Jagged','TGFb','DELTA','CHD1L','Goosecoid','Hypoxia']
signals_new = ['DSH','Jagged','TGFb','DELTA','HIF1a']

n = 4
for i in range(n):
	reduction.edge_red(G)
	gprops.set_edge_props(G)
	gprops.lone_reg(G)
	reduction.homog_node(G,signals_new)
	reduction.node_collapse(G,signals_new)
	#gprops.set_edge_type(G)

gprops.set_edge_props(G)
#outf = '/home/parul/codes/EMT_complt/reduced_minConstrnt.graphml'
#nx.write_graphml(G,outf)
H = nx.DiGraph()
motifs = [[],[]]
for source in G.nodes():
	s = subgraph.find_sg_allpath(G,source,source)
	if s is not None:
		print s,'motif at',source
	if s=='s' or s=='n':
		motifname = source + '_Motif'
		H.add_node(motifname)
		H.node[motifname]['label']=motifname
		motifs[0].append(source)
		motifs[1].append(s)
		
sources = ['SUFU','PDGFR','FGFR','DSH','Jagged','TGFb','DELTA','HIF1a','HGF','IGF1','EGF','CHD1L','Goosecoid']

for ini in sources:
	H.add_node(ini)
	H.node[ini]['label']=ini
	for m in motifs[0]:
		mind = motifs[0].index(m)
		mtype = motifs[1][mind]
		snew = subgraph.find_sg_allpath(G,ini,m)
		if snew == mtype:
			mname = m + '_Motif'
			if snew == 's':
				etype = 'on_state'
			elif snew == 'n':
				etype = 'off_state'
			H.add_edge(ini,mname,etype=etype)
			print snew,'relationship found between',ini,'and',m
			
			
houtf = '/home/parul/Dropbox/codes/EMT_complt/bcb.graphml'
#nx.write_graphml(H,houtf)