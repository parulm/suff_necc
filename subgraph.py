#Header comment(s): 1. The subgraph finding method assumes the first edge of the path as the relationship type. It does not explore the possibility of first edge itself being the subgraph e.g., the first edge is n, the next node has one more n regulator and the source is sufficient for this regulator but since we start scanning from the first edge, it just tries to find an n relationship. This is a crucial problem for finding subgraphs from multiple nodes to multiple nodes.

import networkx as nx

import importlib
import path

#Recursive subgraph finding function - needs review and testing. It seemed to get stuck in an infinite loop if we do not mark the nodes as visited; but if we do, it cannot look at a path which just intersects at a few nodes with a path that has already been visited.
def find_sg(G,inode,onode,nodelist,rasta):
	print 'rasta is:',rasta
	flag = 0
	print 'Looking for paths first'
	#print 'Following are the paths:'
	#for route in ways:
	#	print route
	roads = nx.all_simple_paths(G,inode,onode)
	roads = list(roads)
	ways = sorted(roads, lambda x,y: 1 if len(x)>len(y) else -1 if len(x)<len(y) else 0)
	for rote in ways:
		#print rote
		if rote in rasta:
			continue
		ptype = path.path_type(G,rote)
		if ptype is not None:
			print 'Path found between',inode,'and',onode,'not looking for subgraph.'
			flag = 1
			return ptype

	if flag==0:
		print 'Path not found, trying to look for subgraphs'
		flag2 = 0
		print 'Scanning each path between',inode,'and',onode
		for route in ways:
			if route in rasta:
				print 'This path is already flagged, will not scan this'
				continue
			#if len(route)>6:
			#	continue
			#print 'Inside route scanning'
			print 'Looking at path:', route
			rel = 's/n'
			for i in range(len(route)-1):
				if rel is None:
					print 'There is no relationship on this path, will look at other paths now.'
					break
				print 'Looking at edge',route[i],'->',route[i+1]
				etype = G[route[i]][route[i+1]]['edge_attr']
				new_rel = path.add(rel,etype)
				if new_rel is not None:
					print 'Path until now, cool.'
					rel = new_rel
					continue
				else:
					print 'Could not add the relationship with the edge type.'
					print 'Will look for subgraphs from',inode,'to',route[i+1]
					srel = sg_add(rel,etype)
					regs = G.predecessors(route[i+1])
					print 'Scanning the regulators'
					for r in regs:
						print 'Looking at regulator',r,'of',route[i+1]
						if r == route[i]:
							print 'We came via this regulator, must skip this.'
							continue
						#elif r in route:
						#	print 'This regulator is already in the path, so while looking for paths or subgraphs from',inode,'to',r,'we must avoid taking the same path.'
						rasta.append(route)
						sg_rel = find_sg(G,inode,r,nodelist,rasta)
						if sg_rel is None:
							print 'Could not find needed subgraph, will move on to next path.'
							rel = None
							break
						sg_etype = G[r][route[i+1]]['edge_attr']
						if sg_add(sg_rel,sg_etype)==srel:
							print 'Could find a suitable subgraph from',inode,'to',r
							rel = srel
						else:
							print 'Subgraph found but not of required type, will move on to next path.'
							rel = None
							break
			if rel is not None:
				print 'Found a subgraph during the last path scan.'
				print 'It is on the path:',route
				flag2 = 1
				return rel
		if flag2 == 0:
			print 'Could not find any subgraph during any scan. Sorry.'
			return None

#Recursively and mostly exhaustive - but it seems to take either infinite time or gets stuck in infinite loop. This function needs inspection.
def find_subgraph(G,inode,onode,source,relationship,nodelist):
	print 'Trying to find a subgraph from',inode,'to',onode,'considering that',source,'is the main source.'
	#the following code is to reduce redundancy and keep track of what we're visitng. If you are uncommenting the below lines, modify the function to also read the parameter nodelist which is nX3 array storing node id/names, status of being visited and relationship of the node with source
	ind = nodelist[0].index(inode)
	if nodelist[1][ind]==1:
		print 'Already scanned',inode
		return None
	nodelist[2][ind]=relationship
	neighbors = G.successors(inode)
	print 'Scanning the successors of',inode
	for child in neighbors:
		print 'Looking at',child
		ch_ind = nodelist[0].index(child)
		if nodelist[1][ch_ind]==1:
			continue
		etype = G[inode][child]['edge_attr']
		if path.add(relationship,etype)==None:
			print 'Looking for a subgraph from',source,'to',child
			rel_n = sg_add(relationship,etype)
			if is_subgraph(G,source,child,inode,rel_n,nodelist):
				print 'Found a subgraph.'
				rel_new = rel_n
				pass
			else:
				print 'Marking',child,'as visited.'
				nodelist[1][ch_ind]=1
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
		#elif find_subgraph(G,child,onode,source,rel_new,nodelist) is None:
		#		continue
		else:
			print 'Target not found yet. Looking deeper.'
			return find_subgraph(G,child,onode,source,rel_new,nodelist)
	if nodelist[1][ind]==0:
		print 'Marking',inode,'as visited.'
		nodelist[1][ind]=1
	return None

#A support function used by find_subgraph function. It returns True if it could find a subgraph from source to target. Might contain some major flaws.
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
			if stype==None:
				ans = False
			else:
				print 'Abiding subgraph found!'
				ans = True
			break
	return ans

#Returns the possible kind of subgraph we can have if we have edge_type edge preceded by path / subgraph of type relationship. This function is used at multiple points in this and other files.
def sg_add(relationship,edge_type):
	if path.add(relationship,edge_type)!=None:
		#print 'Error running sg_add. It seems there is a path while you are trying to look for a subgraph'
		return None
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
			sg_rel = None
			#print 'You seem to have a typo, new edge attribute or broken code!'
	return sg_rel

#Finds the shortest path between inode and onode. Try to add each edge of that path sequentially. If at a point, you cannot add the edge, try to find paths to each of the regulators, if yes, fine, else no subgraph. Finds only simple subgraphs. SOMEWHAT based on the idea that if there is a subgraph of one type between a pair of nodes, there cannot be a subgraph of a different type.
def find_sg_by_path(G,inode,onode):
	if not nx.has_path(G,inode,onode):
		#print 'No directed connection'
		return None
	if inode!=onode:
		route = nx.shortest_path(G,inode,onode)
	else:
		#print 'Same source and sink, will pick the shortest path.'
		roads = nx.all_simple_paths(G,inode,onode)
		roads = list(roads)
		path_list = sorted(roads, lambda x,y: 1 if len(x)>len(y) else -1 if len(x)<len(y) else 0)
		#path_list = list(nx.all_simple_paths(G,inode,onode))
		if len(path_list)<=1:
			return None
		route = path_list[1]
	rel = 's/n'
	#print 'We will be scanning',route
	for i in range(len(route)-1):
		#print 'You got into the edge scanning loop'
		#print 'Looking at edge',route[i],'->',route[i+1]
		etype = G[route[i]][route[i+1]]['edge_attr']
		new_rel = path.add(rel,etype)
		if new_rel is not None:
			rel = new_rel
			continue
		else:
			#print 'Could not add the relationship with the edge type.'
			#print 'Will look for subgraphs from',inode,'to',route[i+1]
			srel = sg_add(rel,etype)
			#print 'Adding',rel,'and',etype,'gives',srel
			regs = G.predecessors(route[i+1])
			#print 'Scanning the regulators'
			if len(regs)<=1:
				rel = None
			#print 'We got',len(regs),'regulators of',route[i+1]
			for r in regs:
				#print 'You got into the regulator scanning loop'
				#print 'Looking at regulator',r,'of',route[i+1]
				if r == route[i]:
					#print 'We came via this regulator, must skip this.'
					continue
				if not nx.has_path(G,inode,r):
					#print 'No path from',inode,'to',r
					rel = None
				for p in nx.all_simple_paths(G,inode,r):
					#print 'You got into the paths to regulator scanning loop.'
					ptype = path.path_type(G,p)
					if ptype is None:
						rel = None
					rtype = G[r][route[i+1]]['edge_attr']
					if sg_add(ptype,rtype)==srel:
						#print 'Suitable path found. It is:',p,'of type',ptype
						rel = srel
						#print 'Subgraph is type',rel
						if rel is not None:
							break
					else:
						rel = None
				if rel==None:
					break
				#print 'For regulator',r,'relationship is',rel
	#print 'Just before returning, rel is',rel
	return rel

#Does the same as find_sg_by_path but scans all paths instead of scanning just the shortest one. It breaks and returns as soon as it finds a subgraph (doesn't scan the other paths). This is troublesome for scanning nodes which are driver nodes for more than one motif. I THINK it should be fine for finding subgraphs between different nodes on the basis of Proposition 6 (from theory) being true.
def find_sg_allpath(G,inode,onode):
	issg = False
	rel = None
	#print 'scanning',onode
	if not nx.has_path(G,inode,onode):
		#print 'No directed connection'
		return None
	roads = nx.all_simple_paths(G,inode,onode)
	roads = list(roads)
	path_list = sorted(roads, lambda x,y: 1 if len(x)>len(y) else -1 if len(x)<len(y) else 0)
	#print 'we got',len(path_list),'routes to scan'
	count = 1
	for route in path_list:
		#print 'scanning route number', count
		rel = 's/n'
		#print 'We will be scanning',route
		for i in range(len(route)-1):
			#print 'You got into the edge scanning loop'
			#print 'Looking at edge',route[i],'->',route[i+1]
			etype = G[route[i]][route[i+1]]['edge_attr']
			new_rel = path.add(rel,etype)
			if new_rel is not None:
				rel = new_rel
				continue
			else:
				issg = True
				#print 'Could not add the relationship with the edge type.'
				#print 'Will look for subgraphs from',inode,'to',route[i+1]
				srel = sg_add(rel,etype)
				#print 'Adding',rel,'and',etype,'gives',srel
				regs = G.predecessors(route[i+1])
				#print 'Scanning the regulators'
				if len(regs)<=1:
					rel = None
				#print 'We got',len(regs),'regulators of',route[i+1]
				for r in regs:
					#print 'You got into the regulator scanning loop'
					#print 'Looking at regulator',r,'of',route[i+1]
					if r == route[i]:
						#print 'We came via this regulator, must skip this.'
						continue
					if not nx.has_path(G,inode,r):
						#print 'No path from',inode,'to',r
						rel = None
					for p in nx.all_simple_paths(G,inode,r):
						#print 'You got into the paths to regulator scanning loop.'
						ptype = path.path_type(G,p)
						if ptype is None:
							rel = None
							continue
						rtype = G[r][route[i+1]]['edge_attr']
						if sg_add(ptype,rtype)==srel:
							#print 'Suitable path found. It is:',p,'of type',ptype
							rel = srel
							#print 'Subgraph is type',rel
							if rel is not None:
								break
						else:
							rel = None
					if rel==None:
						break
					#print 'For regulator',r,'relationship is',rel
		#print 'Just before returning, rel is',rel
		count+=1
		if rel is not None:
			print 'path is:',route
			#print 'with relationship', rel
			if issg:
				print 'It was a subgraph!'
			return rel
	return rel


#Finds subgraphs from a group of nodes to another group of nodes. Useful to find motifs with multiple number of driver nodes. The reltypes and oldreltypes lists are important. Add comments on the entire code of this function. Test running this function made me realize some flaw in the general subgraph finding method. See header comment 1.
def find_sg_multiple(G,inode_list,onode_list):
	#print 'Input node list:',inode_list
	#print 'Output node list:', onode_list
	#start = inode_list[0]
	oldreltypes = ['s','n','si','ni','s/n','s/ni']
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
			prev_rel = 's/n'
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



