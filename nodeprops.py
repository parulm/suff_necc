import networkx as nx

import path
import subgraph

def set_node_by_path(G,source,nodelist):
	for node in G.nodes():
		if nx.has_path(G,source,node):
			p = nx.shortest_path(G,source,node)
		else:
			continue
		#print node,'path:',p
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
