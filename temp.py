import networkx as nx
import importlib
import path
import gprops
import reduction
import subgraph

#import infer
#infer.G.remove_edge('ROS','Stomatal closure')
#infer.G.remove_edge('cADPR','Stomatal closure')
#infer.G.remove_edge('Ca2+','SLAC1')
#infer.G.remove_edge('ROS','NO')
#infer.G.remove_edge('Ca2+','NO')
#infer.G.remove_edge('Ca2+','pHc')
#infer.G.remove_edge('S1P','Ca2+')
#infer.G.remove_edge('pHc','RBOH')
#infer.G.remove_edge('NO','M4')
#infer.G.remove_edge('ABA','PI3P5K')
#infer.G.remove_edge('ABA','RBOH')
#infer.G.remove_edge('ABA','8-nitro-cGMP')
#infer.G.remove_edge('ABA','Vacuolar acidification')

#print subgraph.find_sg_allpath(infer.G, 'Ca2+', 'SLAC1')


rulefile = '/home/parul/Dropbox/networks/suff-necc/inference/ABA_new/rules/man.txt'
outfile = '/home/parul/Dropbox/networks/suff-necc/inference/ABA_new/networks/manuscript_red.graphml'

G = importlib.read_boolean(rulefile)
gprops.set_edge_type(G)
gprops.set_edge_props(G)
gprops.lone_reg(G)
reduction.edge_red(G)
gprops.set_edge_props(G)

critical = ['Ca2+', 'ROS', 'OST1', 'PA', 'ABI1']
sigs = []

for node in G.nodes():
	parents = G.predecessors(node)
	if len(parents)<1:
		sigs.append(node)
		
#print 'Signals are:', sigs

critical = critical + sigs

'''
critical = G.nodes()

s = ''
for i in range(10):
	critical.remove(s+str(i+1))
'''

gprops.lone_reg(G)
reduction.node_red(G, critical)
gprops.set_edge_props(G)
gprops.lone_reg(G)
reduction.edge_red(G)
gprops.set_edge_props(G)
nx.write_graphml(G,outfile)

#print subgraph.find_sg_allpath(G, 'ABA', 'Ca2+')


'''
for p in nx.all_simple_paths(infer.G,'ROS','Stomatal closure'):
	#print p
	if path.path_type(infer.G,p) is not None:
		print p
'''