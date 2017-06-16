import networkx as nx
import importlib
import gprops
import reduction

def create_node(G,node,node_list):
	G.add_node(node)
	G.node[node]['label']=node
	node_list.append(node)
	return None

fname = '/home/parul/Dropbox/networks/suff-necc/inference/ABA_new/rules/ABA_5_temp.txt'
outf = '/home/parul/Dropbox/networks/suff-necc/inference/ABA_new/networks/ABA_7_temp.graphml'
G = nx.DiGraph()
node_list = []

f = open(fname,'r+')
lines = f.readlines()
#l = len(lines)
#f.seek(0)

for line in lines:
	#print line
	words = line.split('\t')
	if words[0][0] is '#':
		continue
	source = words[0]
	target = words[1]
	etype = words[2].strip()
	if source not in node_list:
		create_node(G,source,node_list)
	if target not in node_list:
		create_node(G,target,node_list)
	G.add_edge(source,target,edge_attr = etype)

f.close()
gprops.set_edge_props(G)
gprops.lone_reg(G)
reduction.edge_red(G)
gprops.set_edge_props(G)
#nx.write_graphml(G,outf)

'''
critical = ['Ca2+', 'ROS', 'OST1', 'PA', 'ABI1']
sigs = []

for node in G.nodes():
	parents = G.predecessors(node)
	if len(parents)<1:
		sigs.append(node)
		
print 'Signals are:', sigs

critical = critical + sigs
'''

critical = G.nodes()

s = 'M'
for i in range(10):
	critical.remove(s+str(i+1))

print 'Critical is:', critical


gprops.lone_reg(G)
reduction.node_red(G, critical)
gprops.set_edge_props(G)
gprops.lone_reg(G)
reduction.edge_red(G)
gprops.set_edge_props(G)
nx.write_graphml(G,outf)


'''
gprops.update_graph(G, 'MRP5','ON')
gprops.set_edge_props(G)
gprops.lone_reg(G)
reduction.edge_red(G)
gprops.set_edge_props(G)
nx.write_graphml(G,outf)
'''