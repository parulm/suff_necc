#Defines the graph properties

import networkx as nx
import pydot
import pygraphviz

import importlib

#Returns a graph neatly read from a gml file in the updated format. Ref: stackoverflow: 32895291. Use gml_format.sh to correct the format.
def importgraph(file_name):
	G = nx.DiGraph()
	G = importlib.gml2dot(file_name)
	return G

#Setting the edge attribute so that every time we do not have to read and combine both color and arrowhead type. This function reads a graph and sets a new edge attribute named edge_attr to s/n, s/ni, s, n, si or ni. It returns the edited graph. The returned graph may or may not be used; thanks to automatic pass by reference in python.
def set_edge_type(G):
	print 'Setting edge attribute from color and arrow types ...'
	for edge in G.edges():
		arr = G.get_edge_data(*edge)
		u = edge[0]
		v = edge[1]
		col = arr['color']
		etype = arr['arrowhead']
		if col=='red':
			if etype=='normal':
				G[u][v]['edge_attr']='s'
			elif etype=='tee':
				G[u][v]['edge_attr']='si'
		elif col=='blue':
			if etype=='normal':
				G[u][v]['edge_attr']='n'
			elif etype=='tee':
				G[u][v]['edge_attr']='ni'
		elif col=='black':
			if etype=='normal':
				G[u][v]['edge_attr']='s/n'
			elif etype=='tee':
				G[u][v]['edge_attr']='s/ni'
	print 'Done.'            
	return G

#Takes a graph and prints at which nodes homogeneity is not being satisfied. Returns nothing in any case.
def test_homog(G):
	for node in G.nodes():
		regulators = G.predecessors(node)
		old_type = G[regulators[0]][node]['edge_attr']
		for r in regulators:
			new_type = G[r][node]['edge_attr']
			if new_type!=old_type:
				if new_type=='s' and old_type=='ni':
					continue
				elif new_type=='ni' and old_type=='s':
					continue
				elif new_type=='n' and old_type=='si':
					continue
				elif new_type=='si' and old_type=='n':
					continue
				else:
					print 'Homogeneity is not being satisfied at node ',node
					break
				
	return None

#Takes a graph and a node of the graph, returns True if homogeneity is being satisfied at the node, else returns False.
#Possible fixes: print error if the given node is not in the given graph and terminate execution.
def node_homog(G,node):
	regulators = G.predecessors(node)
	old_type = G[regulators[0]][node]['edge_attr']
	for r in regulators:
		new_type = G[r][node]['edge_attr']
		if new_type!=old_type:
			if new_type=='s' and old_type=='ni':
				continue
			elif new_type=='ni' and old_type=='s':
				continue
			elif new_type=='n' and old_type=='si':
				continue
			elif new_type=='si' and old_type=='n':
				continue
			else:
				return False
		#old_type = new_type
	return True

#Sets color and arrowhead type on the basis of the edge attribute edge_attr. Multiple functions edit the edge attribute while adding or modifying edges but do not update the color and arrow type. This is required to correctly view the graph when imported to graphml. Function modifies the graph and returns None.
def set_edge_props(G):
	print 'Setting graphic properties of edges ...'
	for node in G.nodes():
		regulators = G.predecessors(node)
		for r in regulators:
			etype = G[r][node]['edge_attr']
			if etype=='s':
				G[r][node]['color']='red'
				G[r][node]['arrowhead']='normal'
			elif etype=='si':
				G[r][node]['color']='red'
				G[r][node]['arrowhead']='tee'
			elif etype=='n':
				G[r][node]['color']='blue'
				G[r][node]['arrowhead']='normal'
			elif etype=='ni':
				G[r][node]['color']='blue'
				G[r][node]['arrowhead']='tee'
			elif etype=='s/n':
				G[r][node]['color']='black'
				G[r][node]['arrowhead']='normal'
			elif etype=='s/ni':
				G[r][node]['color']='black'
				G[r][node]['arrowhead']='tee'
	print 'Done.'
	return None

#Sets node type on a given graph. Node type is red if it's regulators are related by OR rule. It is blue if they are related by AND rule. Function modifies the graph and returns None.
def set_node_type(G):
	print 'Setting node types for all nodes'
	print 'This function must be run after testing for Homogeneity!'
	for node in G.nodes():
		regulator = G.predecessors(node)[0]
		ntype = G[regulator][node]['edge_attr']
		if ntype=='s' or ntype=='ni':
			node_color = 'red'
		elif ntype=='n' or ntype=='si':
			node_color = 'blue'
		elif ntype=='s/n' or ntype=='s/ni':
			node_color = 'black'
		
		G.node[node]['ncolor']=node_color
	print 'Done.'
	return None

#Takes a graph and it's node and returns the node type. Node type is red if its' regulators are related by OR rule, blue if AND rule and black if the node takes a single regulator.
def node_type(G,node):
	regulator = G.predecessors(node)[0]
	ntype = G[regulator][node]['edge_attr']
	if ntype=='s' or ntype=='ni':
		node_color = 'red'
	elif ntype=='n' or ntype=='si':
		node_color = 'blue'
	elif ntype=='s/n' or ntype=='s/ni':
		node_color = 'black'
	return node_color

#Takes a graph and sets all single regulator nodes' edges as s/n or s/ni depending on what the original edge was. For example if A-B is si and A is the only regulator, this function sets A-B as s/ni. Returns the modified graph.
def lone_reg(G):
	print 'Setting all single regulator nodes as suff/necc or inhibitory suff/necc ...'
	for node in G.nodes():
		regs = G.predecessors(node)
		if len(regs)==1:
			parent = regs[0]
			if G[parent][node]['edge_attr']=='s/n' or G[parent][node]['edge_attr']=='s/ni':
				break
			if G[parent][node]['arrowhead']=='normal':
				newt = 's/n'
			elif G[parent][node]['arrowhead']=='tee':
				newt = 's/ni'
			print 'Setting edge',parent,'->',node, 'as',newt
			G[parent][node]['edge_attr']=newt
			
	print 'Done'
	return G

