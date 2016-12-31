import networkx as nx
import importlib
import gprops

fname = '/home/parul/Dropbox/codes/rules/EMT_complt/main.txt'

G = importlib.read_boolean(fname)
gprops.set_edge_type(G)
gprops.set_node_type(G)

GLI = ['GLI','SHH','Patched','SMO','FUS','SUFU']
TGFb_SNAI1 = ['TGFb','TGFbR','CDC42','PAK1','SNAI1']
RAS = ['RAS','PI3K','AKT','GSK3beta']
ERK = ['ERK','RKIP','c-fos','EGR1','SNAI1','MEK']
Jagged = ['SMAD','Jagged','NOTCH','NOTCH_ic','Csl','SNAI1','ZEB1','9','7','miR200','TGFb','TGFbR','6']
Delta = ['DELTA','SMAD','NOTCH','NOTCH_ic','Csl','SNAI1','ZEB1','9','7','miR200','TGFb','6','SHH','Patched','SMO','FUS','SUFU','GLI','Wnt','Frizzled','DSH','GSK3beta','RAS']
bcatnuc = ['betacatenin_nuc','TCF/LEF','GLI','SHH','Patched','SMO','FUS','SUFU','3','Wnt','Frizzled','DSH','GSK3beta','1','2','Dest_compl','betacatenin_memb']
DSH = ['SMAD','SNAI1','ZEB1','9','7','miR200','TGFb','6','SHH','Patched','SMO','FUS','SUFU','GLI','Wnt','Frizzled','DSH','GSK3beta','RAS','RAF','MEK','ERK','c-fos','EGR1']
subg = ['NOTCH_ic','Csl','SNAI1','miR200','9','ZEB1','4','E-cadherin','FOXC2','SNAI2','HEY1','ZEB2','TWIST1','10']

comm = list(set(GLI) | set(TGFb_SNAI1) | set(RAS) | set(ERK) | set(Jagged) | set(Delta) | set(bcatnuc) | set(DSH))

print comm

outfname = '/home/parul/Dropbox/codes/EMT_complt/use/test.graphml'
nx.write_graphml(G,outfname)

signals = ['SHH','Wnt','HGF','PDGF','IGF1','EGF','FGF','Jagged','TGFb','DELTA','CHD1L','Goosecoid','Hypoxia']

for node in signals:
	G.remove_node(node)

#for node in signals:
#	gprops.update_graph(G,node,'OFF')

print 'Current number of nodes in the network:',len(G.nodes())
print 'Number of nodes in the motifs:',len(comm)

print 'Checking if all motif nodes still there'
cnt = 0
for mnode in comm:
	if mnode not in G.nodes():
		print 'Oh!',mnode,'not in the network!'
		cnt+=1
print 'Total',cnt,'of the',len(comm),'nodes were removed.'

for node in G.nodes():
	if node not in comm:
		print node

'''
for node in G.nodes():
	if node not in subg:
		G.remove_node(node)
		
outfname = '/home/parul/Dropbox/codes/EMT_complt/use/subg_motif.graphml'
nx.write_graphml(G,outfname)
'''