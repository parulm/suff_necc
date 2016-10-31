#Code to read a gml file and output the dot file conserving edge colors and arrowhead type

import networkx as nx
import pydot
import graphviz

#Creates a node. Function for use by other functions, you can ignore this for most part.
def create_node(G,node,node_list):
	#print 'Creating node',node
	G.add_node(node)
	G.node[node]['label']=node
	#add node and knowledge of its update function in array node_list
	node_list[0].append(node)
	node_list[1].append(0)
	return True

#Reads and returns a network from a list of boolean functions. In older versions of this repo, this code is under the file and_or.py.
def read_boolean(filename):
	print 'Creating graph from Boolean rules in',filename,'...'
	G=nx.DiGraph()
	keywds = ['NOT','not','AND','and','OR','or']
	f = open(filename,'r+')
	lines = f.readlines()
	l = len(lines)
	node_list = [[],[]]
	f.seek(0)
	comp=0
	for i in range(l):
		words = f.readline().split()
		if words[0][0] == '#':
			continue
		if words[0].endswith('*'):
			node = words[0][:-1]
			if node not in node_list[0]:
				create_node(G,node,node_list)
			ind = node_list[0].index(node)
			node_list[1][ind] = 1
			#put this node in the list of nodes and mark update function as known
		else:
			print ('Please check the syntax')
			break
		if words[1]=='=':
			j=2
			end_found = True
			crelation = ''
			while j<len(words):
				atending = atbeginning = False
				if words[j].endswith(')'):
					atending = True
					end_found = True
					if not crelation and j+1<len(words):
						crelation=words[j+1]
					words[j] = words[j][:-1]
				if words[j].startswith('('):
					atbeginning = True
					connected = False
					comp+=1
					create_node(G,str(comp),node_list)
					cnode = str(comp)
					words[j] = words[j][1:]
					end_found = False
				if words[j] not in keywds:
					#this must be a node, add it to the list if it's not there
					if words[j] not in node_list[0]:
						create_node(G,words[j],node_list)
					if not end_found or atending:
						tnode = cnode
					elif end_found:
						tnode = node
					next_node = words[j]
					is_inh = 0
					relation = ''
					if j+1<len(words) and not atending:
						relation = words[j+1]
					if (words[j-1]=='NOT' or words[j-1]=='not') and not atbeginning:
						is_inh = 1
						if j>3 and not atbeginning and words[j-2]!='NOT' and words[j-2]!='not' and end_found:
							relation = words[j-2]
					elif words[j-1] in keywds and not atbeginning:
						relation = words[j-1]
					if relation=='AND' or relation=='and':
						if is_inh==0:
							col = 'blue'
						else:
							col = 'red'
					elif relation=='OR' or relation=='or':
						if is_inh==0:
							col = 'red'
						else:
							col = 'blue'
					else:
						col = 'black'
					#add inhibitory edge from next_node to node of color color
					if is_inh==0:
							etype = 'normal'
					elif is_inh==1:
							etype = 'tee'
					G.add_edge(next_node,tnode, color = col, arrowhead = etype)
				if atbeginning and not end_found:
					if words[j-1]=='NOT' or words[j-1]=='not':
						cis_inh = 1
					else:
						cis_inh = 0
					if cis_inh == 0 and words[j-1] in keywds:
						crelation=words[j-1]
					elif cis_inh == 1 and words[j-2] in keywds:
						crelation=words[j-2]
				if crelation:
					if crelation=='AND' or crelation=='and':
						if cis_inh==0:
							ccol = 'blue'
						else:
							ccol = 'red'
					elif crelation=='OR' or crelation=='or':
						if cis_inh==0:
							ccol = 'red'
						else:
							ccol = 'blue'
					else:
						ccol = 'black'
					if cis_inh==0:
							cetype = 'normal'
					elif cis_inh==1:
							cetype = 'tee'
					G.add_edge(cnode,node,color = ccol, arrowhead = cetype)
					connected=True


				j+=1

		else:
			print ('Please enter a file with the correct syntax.')
	print 'Done.'
	return G

#Reads and returns graph from a gml file in the updated gml format.
def gml2dot(fname):

	print 'Importing graph from', fname,'...'

	#Import graph from gml file
	G = nx.DiGraph()
	G = nx.read_gml(fname)

	edge_list = [[],[],[]]

	#Assign node color as readable by dot files and property mapper in yEd.
	l = G.edges()
	for i in l:
		m = G.get_edge_data(*i)
		if m[u'graphics'][u'fill']=='#0000FF':
			edge_color = 'blue'
		elif m[u'graphics'][u'fill']=='#FF0000':
			edge_color = 'red'
		elif m[u'graphics'][u'fill']=='#000000':
			edge_color = 'black'

		if m[u'graphics'][u'targetArrow']=='standard':
			edge_arrow = 'normal'
		elif m[u'graphics'][u'targetArrow']=='t_shape':
			edge_arrow = 'tee'

		edge_list[0].append(i)
		edge_list[1].append(edge_color)
		edge_list[2].append(edge_arrow)


	#Obtain a list of nodes
	n = G.nodes(data=True)
	node_list = []
	for j in n:
		node_list.append(j[0])

	#Create a new graph to save only the required properties (yEd saves a lot of other details we do not want like orientation, position, etc.)
	H = nx.DiGraph()

	#Add all nodes with the labels in the new graph
	for k in node_list:
		H.add_node(k)
		H.node[k]['label'] = k

	#Add all the edges with color and arrow type in the new graph
	noe = G.number_of_edges()
	for i in range(noe):
		e = edge_list[0][i]
		col = edge_list[1][i]
		etype = edge_list[2][i]
		H.add_edge(*e, color = col, arrowhead = etype)

	'''
	dotfname = gmlfile + '.dot'
	nx.drawing.nx_agraph.write_dot(H,dotfname)

	graphmlfname = gmlfile + '.graphml'
	nx.write_graphml(H,graphmlfname)
	'''
	print 'Done.'
	return H
