#Header comment(s): 1. The subgraph finding method assumes the first edge of the path as the relationship type. It does not explore the possibility of first edge itself being the subgraph e.g., the first edge is n, the next node has one more n regulator and the source is sufficient for this regulator but since we start scanning from the first edge, it just tries to find an n relationship. This is a crucial problem for finding subgraphs from multiple nodes to multiple nodes.

import networkx as nx

import path

#Returns the possible kind of subgraph we can have if we have edge_type edge preceded by path / subgraph of type relationship. This function is used at multiple points in this and other files.
def sg_add(relationship,edge_type):
	sg_rel = None
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
	elif relationship=='sn':
		if edge_type=='s':
			sg_rel = 'n'
		elif edge_type=='n':
			sg_rel = 's'
		elif edge_type=='si':
			sg_rel = 'ni'
		elif edge_type=='ni':
			sg_rel = 'si'
	else:
		sg_rel = None
		#print 'You seem to have a typo, new edge attribute or broken code!'
		print 'Error while processing',relationship,'as relationship and',edge_type,'as edge_type'
	return sg_rel


#Finds subgraphs recursively. Variable motif must be True if you inode=onode and we are looking for a cyclic subgraph/path.
def finalsg(G, inode, onode, seen=[], motif=False):
	if inode==onode and not motif:
		return 'sn'
	print 'seen:', seen
	if (inode,onode) in seen:
		print inode,'->',onode,'has been seen'
		print 'Avoiding an infinite recursion'
		return None
	seen.append((inode, onode))
	rel = None
	if not nx.has_path(G, inode, onode):
		print 'No path between', inode, onode
		return None
	pathlist = nx.all_simple_paths(G,inode,onode)
	pathlist = list(pathlist)
	pathlist.sort(key=len)
	for way in pathlist:
		#way = ['A', 'H', 'G', 'D', 'E', 'K']
		print 'Scanning path', way
		if path.path_type(G, way) is not None:
			print 'found a direct path!'
			return path.path_type(G, way)
		print 'No direct logic path. Looking for a subgraph'
		prevetype = 'sn'
		fail = False
		for i in range(len(way)-1):
			if fail:
				rel = None
				break
			newetype = G[way[i]][way[i+1]]['edge_attr']
			rel = path.add(prevetype, newetype)
			srel = None
			if rel==None:
				print 'cannot add edges',prevetype,'at',way[i],'and',newetype,'finding subgraph'
				srel = sg_add(prevetype, newetype)
				print 'there may be a subgraph of type',srel
				regulators = G.predecessors(way[i+1])
				for reg in regulators:
					if reg==way[i]:
						continue
					print 'checking for regulator',reg,'of node', way[i+1]
					ptype = finalsg(G, inode, reg, seen)
					print 'Right after the recursion, ptype is', ptype
					if ptype is None:
						fail = True
						rel = None
						break
					print 'before doing sg_add, ptype is', ptype
					if sg_add(ptype,G[reg][way[i+1]]['edge_attr'])==srel:
						continue
					else:
						fail = True
						rel = None
						break
				if srel is not None and not fail:
					rel = srel
			if rel is not None:
				prevetype = rel
		if rel is not None:
			return rel
	return rel


#Finds subgraphs from a group of nodes to another group of nodes. Useful to find motifs with multiple number of driver nodes. The reltypes and oldreltypes lists are important. Add comments on the entire code of this function. Test running this function made me realize some flaw in the general subgraph finding method. See header comment 1.
def find_sg_multiple(G,inode_list,onode_list):
	#print 'Input node list:',inode_list
	#print 'Output node list:', onode_list
	#start = inode_list[0]
	oldreltypes = ['s','n','si','ni','sn','sni']
	for stop in onode_list:
		reltypes = []
		for start in inode_list:
			#print 'start is:', start, 'stop is:', stop
			roads = nx.all_simple_paths(G,start,stop)
			roads = list(roads)
			path_list = sorted(roads, lambda x,y: 1 if len(x)>len(y) else -1 if len(x)<len(y) else 0)
			if len(path_list)>1:
				if start==stop:
					route = path_list[1]
				else:
					route = path_list[0]
			else:
				continue
			prev_rel = 'sn'
			#print 'Looking at path',route
			for i in range(len(route)-1):
				etype = G[route[i]][route[i+1]]['edge_attr']
				rel = path.add(prev_rel,etype)
				if rel == None:
					#print 'Path cannot be added at',route[i],'to',route[i+1]
					srel = sg_add(prev_rel,etype)
					regs = G.predecessors(route[i+1])
					if len(regs)<=1:
						rel = None
					for regulator in regs:
						if regulator == route[i]:
							continue
						found = False
						for source in inode_list:
							if not nx.has_path(G,source,regulator):
								continue
							for p in nx.all_simple_paths(G,source,regulator):
								ptype = path.path_type(G,p)
								rtype = G[regulator][route[i+1]]['edge_attr']
								if sg_add(ptype,rtype) == srel:
									found = True
									break
							if found:
								break
						if found:
							continue
						else:
							rel = None
					rel = srel
				prev_rel = rel
			reltypes.append(rel)
		#print 'for end point',stop,'stored relationships are:',reltypes
		oldreltypes = list(set(reltypes) & set(oldreltypes))
	return oldreltypes