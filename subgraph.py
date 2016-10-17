import networkx as nx

import importlib
import path

def find_subgraph(G,inode,onode,source,relationship,nodelist):
	#the following code is to reduce redundancy and keep track of what we're visitng. If you are uncommenting the below lines, modify the function to also read the parameter nodelist which is nX3 array storing node id/names, status of being visited and relationship of the node with source
	ind = nodelist[0].index(inode)
	if nodelist[1][ind]==0:
		nodelist[1][ind]=1
	#elif nodelist[1][ind]==1 and inode!=source:
	#	print 'Already scanned',inode
	#	return None
	nodelist[2][ind]=relationship
	neighbors = G.successors(inode)
	print 'Scanning the successors of',inode
	for child in neighbors:
		ch_ind = nodelist[0].index(child)
		if nodelist[1][ch_ind]==0:
			nodelist[1][ch_ind]=1
		else:
			continue
		etype = G[inode][child]['edge_attr']
		if path.add(relationship,etype)=='null':
			print 'Looking for a subgraph from',source,'to',child
			rel_n = sg_add(relationship,etype)
			if is_subgraph(G,source,child,inode,rel_n,nodelist):
				print 'Found a subgraph.'
				rel_new = rel_n
				pass
			else:
				print 'No subgraph found. Looking at the other successors of',inode
				continue
		else:
			print 'Path until now. Cool.'
			rel_new = path.add(relationship,etype)
		nodelist[2][ch_ind]=rel_new
		if child==onode:
			print 'Found the target we were looking for!'
			print source,'->',onode,'subgraph of type',rel_new
			return rel_new
		else:
			print 'Target not found yet. Looking deeper.'
			return find_subgraph(G,child,onode,source,rel_new,nodelist)
	
	return None

def is_subgraph(G,source,target,reg,rel,nodelist):
	#checks if all paths/subgraphs from source to regulators of target are of type which when sg_added to regulator-target edge gives relationship
	print 'Finding if all regulators of',target,'form a subgraph from',source
	regulators = G.predecessors(target)
	for r in regulators:
		rtype = G[r][target]['edge_attr']
		flag=0
		if r is reg:
			continue
		for route in nx.all_simple_paths(G,source,r):
			ptype = path.path_type(G,route)
			sg_type = sg_add(ptype,rtype)
			if sg_type==rel:
				print 'The regulator',r,'of',target,'abides by the subgraph requirement through a path.'
				ans = True
				flag = 1
				break
		if flag==0:
			print 'Subgraph requirement not fulfilled by path, looking for recursive subgraphs'
			sgtype = find_subgraph(G,source,r,source,'s/n',nodelist)
			stype = sg_add(sgtype,rtype)
			if stype=='nothing':
				ans = False
			else:
				print 'Abiding subgraph found!'
				ans = True
			break
	return ans

def sg_add(relationship,edge_type):
	if path.add(relationship,edge_type)!='null':
		#print 'Error running sg_add. It seems there is a path while you are trying to look for a subgraph'
		return 'nothing'
	else:
		if relationship=='s':
			if edge_type=='n':
				sg_rel = 's'
			elif edge_type=='ni':
				sg_rel = 'si'
		elif relationship=='n':
			if edge_type=='s':
				sg_rel = 'n'
			elif edge_type=='si':
				sg_rel = 'ni'
		elif relationship=='si':
			if edge_type=='s':
				sg_rel = 'si'
			elif edge_type=='si':
				sg_rel = 's'
		elif relationship=='ni':
			if edge_type=='n':
				sg_rel = 'ni'
			elif edge_type=='ni':
				sg_rel = 'n'
		else:
			sg_rel = 'nothing'
			#print 'You seem to have a typo, new edge attribute or broken code!'
	return sg_rel