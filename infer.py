import networkx as nx
import importlib
import gprops
#import reduction

def create_node(G,node,node_list):
	G.add_node(node)
	G.node[node]['label']=node
	node_list.append(node)
	return None

fname = 'examples/inference_test.txt'
#outf = 'examples/inferred_ABA_network.graphml'
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
#gprops.lone_reg(G)
#reduction.edge_red(G)
#gprops.set_edge_props(G)
#nx.write_graphml(G,outf)

#print the Boolean rules that have no incompatibility
#create compatibility dictionary
comp = {'s':['s', 'ni'], 'si':['si', 'n'], 'n':['n', 'si'], 'ni':['ni', 's']}

gprops.set_edge_type(G)



for node in G.nodes():
	regs = list(G.predecessors(node))
	if len(regs)==0:
		print str(G.node[node]['label']), 'is a source node'
		continue
	if len(regs)==1:
		print str(G.node[node]['label'])+'* = '+str(G.node[regs[0]]['label'])
	else:
		dom = G[regs[0]][node]['edge_attr']
		if dom[-1]=='i':
			rule_so_far = 'not '+str(G.node[regs[0]]['label'])
		else:
			rule_so_far = str(G.node[regs[0]]['label'])
		rule_opp = ''
		compatible = True
		for regulator in regs[1:]:
			logic = G[regulator][node]['edge_attr']
			#compatible = True
			if logic not in comp[dom]:
				compatible = False
				if rule_opp:
					if dom[0]=='s':
						rule_opp+=' and '
					else:
						rule_opp+=' or '
					if logic[-1]=='i':
						rule_opp+='not '
				rule_opp+=str(G.node[regulator]['label'])
				#break
			else:
				if logic[-1]=='i':
					if logic[0]=='s':
						rule_so_far+=(' and not '+str(G.node[regulator]['label']))
					else:
						rule_so_far+=(' or not '+str(G.node[regulator]['label']))
				else:
					if logic[0]=='s':
						rule_so_far+=(' or '+str(G.node[regulator]['label']))
					else:
						rule_so_far+=(' and '+str(G.node[regulator]['label']))
		if compatible:
			print str(G.node[node]['label'])+'* = '+rule_so_far
		else:
			print 'Regulators of', str(G.node[node]['label']), 'are incompatible.',
			#print 'One set of regulators are:', rule_so_far
			#print 'Second set of regulators are:', rule_opp
			if dom=='s' or dom=='ni':
				#rule_so_far is OR type
				final_rule1 = '('+rule_opp+')'+' or '+rule_so_far
				final_rule2 = rule_opp+' and '+'('+rule_so_far+')'
			else:
				final_rule1 = '('+rule_opp+')'+' and '+rule_so_far
				final_rule2 = rule_opp+' or '+'('+rule_so_far+')'
			print 'Rules as per the two templates are: \n1.',final_rule1, '\n2.', final_rule2 
print 'Done creating all Boolean rules'





'''
critical = ['Ca2+', 'ROS', 'OST1', 'PA', 'ABI1']
sigs = []

for node in G.nodes():
	parents = G.predecessors(node)
	if len(parents)<1:
		sigs.append(node)
		
print 'Signals are:', sigs

critical = critical + sigs


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

'''
#nx.write_graphml(G,outf)


'''
gprops.update_graph(G, 'MRP5','ON')
gprops.set_edge_props(G)
gprops.lone_reg(G)
reduction.edge_red(G)
gprops.set_edge_props(G)
nx.write_graphml(G,outf)
'''