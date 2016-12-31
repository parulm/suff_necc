import networkx as nx
import importlib
import reduction
import subgraph
import gprops

fname = '/home/parul/Dropbox/codes/rules/EMT_complt/main.txt'

G = importlib.read_boolean(fname)
gprops.set_edge_type(G)
gprops.set_node_type(G)

'''
signals = ['SHH','Wnt','HGF','PDGF','IGF1','EGF','FGF','Jagged','TGFb','DELTA','CHD1L','Goosecoid','Hypoxia']
signals_new = ['DSH','Jagged','TGFb','DELTA','HIF1a']
signals_output = ['DSH','Jagged','TGFb','DELTA','HIF1a','EMT']

n = 4
for i in range(n):
	reduction.edge_red(G)
	gprops.set_edge_props(G)
	gprops.lone_reg(G)
	reduction.homog_node(G,signals_output)
	reduction.node_collapse(G,signals_output)
	#gprops.set_edge_type(G)

gprops.set_edge_props(G)
outf = '/home/parul/Dropbox/codes/EMT_complt/reduced_in-outConstrnt.graphml'
#nx.write_graphml(G,outf)
'''
print 'Testing the function on multiple driver nodes'
ilist = ['ERK','SMAD']
olist = ['SMAD','ERK']
print subgraph.find_sg_multiple(G,ilist,olist)

for i in G.nodes():
	for j in G.nodes():
		if i!=j:
			nlist = [i,j]
			relfound = subgraph.find_sg_multiple(G,nlist,nlist)
			if 's' in relfound or 'n' in relfound:
				print i,j,relfound

'''
H = nx.DiGraph()
motifs = [[],[]]
print 'Finding motifs'
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

print 'Signals to motifs'
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

print 'Motifs to motifs'
for m1 in motifs[0]:
	m1name = m1 + '_Motif'
	for m2 in motifs[0]:
		motif_rel = subgraph.find_sg_allpath(G,m1,m2)
		m2name = m2 + '_Motif'
		if motif_rel is not None:
			if motif_rel=='s' or motif_rel=='si':
				etype = 'on_state'
			elif motif_rel=='n' or motif_rel=='ni':
				etype = 'off_state'
			H.add_edge(m1name,m2name,etype=etype)
			print motif_rel,'relationship found between',m1,'and',m2

print 'Motifs to sink'
sink = 'EMT'
for m in motifs[0]:
	mind = motifs[0].index(m)
	mtype = motifs[1][mind]
	reltype = subgraph.find_sg_allpath(G,m,sink)
	if reltype == mtype:
		mname = m + '_Motif'
		if reltype == 's':
			etype = 'on_state'
		elif reltype == 'n':
			etype = 'off_state'
		H.add_edge(mname,sink,etype=etype)
		print reltype,'relationship found between',m,'and',sink
			
			

houtf = '/home/parul/Dropbox/codes/EMT_complt/bcb.graphml'
nx.write_graphml(H,houtf)
'''