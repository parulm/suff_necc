import networkx as nx

import path
import subgraph

def set_node_by_path(G,source,nodelist):
	for node in G.nodes():
		if nx.has_path(G,source,node):
			#print 'There is a path to',node
			if node!=source:
				p = nx.shortest_path(G,source,node)
			else:
				#print node,'and',source,'are the same.'
				path_list = list(nx.all_simple_paths(G,source,node))
				#print path_list
				if len(path_list)<=1:
					continue
				p = path_list[1]
		else:
			#print 'Found no path from',source,'to',node
			continue
		#print node,'path:',p
		#print 'Path from',source,'to',node,'is:',p
		ptype = path.path_type(G,p)
		nind = nodelist[0].index(node)
		if ptype is not None:
			print 'Setting node',node,'to relationship status',ptype
			nodelist[1][nind] = 1
			nodelist[2][nind] = ptype

	return None

def set_node_by_sg(G,source,nodelist):
	for node in G.nodes():
		nind = nodelist[0].index(node)
		if nodelist[1][nind]==1:
			continue
		if not nx.has_path(G,source,node):
			continue
		srel = subgraph.find_sg_by_path(G,source,node)
		if srel is not None:
			print 'Setting node',node,'to relationship status',srel
			nodelist[1][nind] = 1
			nodelist[2][nind] = srel
	return None

def nodeprp_path(G,inode,onode,nodelist):
	if nx.has_path(G,inode,onode):
		p = nx.shortest_path(G,inode,onode)
	else:
		return None
	#print node,'path:',p
	ptype = path.path_type(G,p)
	nind = nodelist[0].index(onode)
	if ptype is not None:
		print 'Setting node',onode,'to relationship status',ptype
		nodelist[1][nind] = 1
		nodelist[2][nind] = ptype

	return None

def nodeprp_sg(G,inode,onode,nodelist):
	if not nx.has_path(G,inode,onode):
		return None
	srel = subgraph.find_sg_by_path(G,inode,onode)
	if srel is not None:
		nind = nodelist[0].index(onode)
		print 'Setting node',onode,'to relationship status',srel
		nodelist[1][nind] = 1
		nodelist[2][nind] = srel
	return None

def set_node_allpath(G,source,nodelist):
	for node in G.nodes():
		if not nx.has_path(G,source,node):
			continue
		for p in nx.all_simple_paths(G,source,node):
			#print node,'path:',p
			#print 'Path from',source,'to',node,'is:',p
			ptype = path.path_type(G,p)
			nind = nodelist[0].index(node)
			if ptype is not None:
				print 'Setting node',node,'to relationship status',ptype
				nodelist[1][nind] = 1
				nodelist[2][nind] = ptype
				break

	return None
