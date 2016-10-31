#Defines the graph properties

import networkx as nx
import pydot
import pygraphviz
from time import sleep

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
		if len(G.predecessors(node))==0:
			node_color = 'black'
			continue
		#print G.predecessors(node)
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
	if len(G.predecessors(node))==0:
		return 'black'
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
	#print 'Setting all single regulator nodes as suff/necc or inhibitory suff/necc ...'
	#print G.nodes()
	for node in G.nodes():
		#print node
		#if node=='FLIP':
		#	print 'Yes, we scanned',node
		regs = G.predecessors(node)
		if len(regs)==1:
			parent = regs[0]
			if G[parent][node]['edge_attr']=='s/n' or G[parent][node]['edge_attr']=='s/ni':
				continue
			if G[parent][node]['arrowhead']=='normal':
				newt = 's/n'
			elif G[parent][node]['arrowhead']=='tee':
				newt = 's/ni'
			print 'Setting edge',parent,'->',node, 'as',newt
			G[parent][node]['edge_attr']=newt
			
	print 'Done'
	return G

#Takes a graph, a node and the initial / fixed state we are setting the node to. This function by itself updates everything that logically follows from the fixed state of the given node. This might leave some stray nodes though.
def update_graph(G,node,node_status):
	print 'Setting',node,'to',node_status
	if node=='Apoptosis':
		print 'WOAH WOAH WOAH!!! WAIT!!!!! You just got Apoptosis!'
		print 'Giving you a couple seconds to grasp what just happened'
		sleep(3)
	if node not in G.nodes():
		print 'Error!',node,'not in the graph.'
		return None
	children = G.successors(node)
	if node_status=='ON':
		for child in children:
			if child not in G.nodes():
				continue
			if child==node:
				continue
			crel = G[node][child]['color']
			parents = G.predecessors(child)
			if len(parents)==2:
				for p in parents:
					if p!=node:
						parent = p
				arrtype = G[parent][child]['arrowhead']
				if arrtype=='normal':
					print 'Setting',parent,'->',child,'as s/n'
					G[parent][child]['edge_attr'] = 's/n'
				elif arrtype=='tee':
					print 'Setting',parent,'->',child,'as s/ni'
					G[parent][child]['edge_attr'] = 's/ni'
				else:
					print 'Error! Set edge properties first. Use function gprops.set_edge_props'
			if crel=='red' or crel=='black':
				if G[node][child]['edge_attr']=='s' or G[node][child]['edge_attr']=='s/n':
					update_graph(G,child,'ON')
				elif G[node][child]['edge_attr']=='si' or G[node][child]['edge_attr']=='s/ni':
					update_graph(G,child,'OFF')
			#set all sufficiently related children to their updated state. Use a nodelist or use this function recursively.
	elif node_status=='OFF':
		for child in children:
			if child not in G.nodes():
				continue
			if child==node:
				continue
			crel = G[node][child]['color']
			parents = G.predecessors(child)
			if len(parents)==2:
				for p in parents:
					if p!=node:
						parent = p
				arrtype = G[parent][child]['arrowhead']
				if arrtype=='normal':
					G[parent][child]['edge_attr'] = 's/n'
				elif arrtype=='tee':
					G[parent][child]['edge_attr'] = 's/ni'
				else:
					print 'Error! Set edge properties first. Use function gprops.set_edge_props'
			if crel=='blue' or crel=='black':
				if G[node][child]['edge_attr']=='n' or G[node][child]['edge_attr']=='s/n':
					update_graph(G,child,'OFF')
				elif G[node][child]['edge_attr']=='ni' or G[node][child]['edge_attr']=='s/ni':
					update_graph(G,child,'ON')
			#set all necessarily related children to ...
	else:
		print 'Error! Node status must be ON or OFF only.'
	#Add code to set the edge type to s/n if there are only two regulators of the child - one of which is being set to a fixed state.
	#Also take care of s/n-ly related children
	print 'Removing node',node
	G.remove_node(node)
	return None

#function to remove stray nodes
def remove_stray(G):
	for node in G.nodes():
		parents = G.predecessors(node)
		children = G.successors(node)
		if len(parents)==0 and len(children)==0:
			print 'Node',node,'is a stray node, removing it.'
			G.remove_node(node)
	return None