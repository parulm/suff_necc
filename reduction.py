#Code to reduce a given sufficient necessary network

import networkx as nx
import pydot
import pygraphviz
import re

import path
import gprops

#Takes a graph and deletes every edge for which a path exists that causes the same effect as the edge i.e. the edge is same type as of the path. This is binary transitive reduction which conforms the logical correctness of reduction. Termed logical binary transitive reduction. Functions returns None.
def edge_red(G):
	print 'Running logical transitive reduction ...'
	elist = list(G.edges())
	for edge in elist:
		u = edge[0]
		v = edge[1]
		if not G.has_edge(u,v):
			continue
		arr = G.get_edge_data(*edge)
		uv_type = arr['edge_attr']
		for route in nx.all_simple_paths(G, source=u, target=v):
			if len(route)<=2:
				continue
			elif path.path_type(G,route)==uv_type:
				print 'Removing edge between',u,'and',v,'by logical transitive reduction because the path',route, 'is also', uv_type
				G.remove_edge(u,v)
				break
			else:
				continue
	print 'Done.'
	return G


#Scans all edges of the network and for a sn or sni edge and collapses that edge if none of the source or target nodes of that edge lies in set critical.
def node_collapse(G,critical=[]):
	rlist = []
	for e in G.edges(data=True):
		if e[0] in critical or e[1] in critical:
			continue
		etype = G[e[0]][e[1]]['edge_attr']
		if etype=='sn' or etype=='sni':
			parents = G.predecessors(e[0])
			for p in parents:
				new_etype = path.add(G[p][e[0]]['edge_attr'],etype)
				G.add_edge(p,e[1],edge_attr=new_etype)
			G.node[e[1]]['label'] = e[0]+e[1]
			rlist.append(e)
	for r in rlist:
		G.remove_node(r[0])


#Collapses two non critical nodes (or one critical node with another non critical node) if they have the same set of in- and out-neighbors with equal corresponding logic implications
def LVC(G, critical=[]):
	toremove = []
	for n1 in G.nodes():
		if n1 in toremove:
			continue
		for n2 in G.nodes():
			if n2 in toremove:
				continue
			if n1==n2:
				continue
			else:
				regs1 = G.predecessors(n1)
				regs2 = G.predecessors(n2)
				targets1 = G.successors(n1)
				targets2 = G.successors(n2)
				flag = False
				if set(regs1)==set(regs2) and set(targets1)==set(targets2):
					flag = True
					for reg in regs1:
						if G[reg][n1]['edge_attr']!=G[reg][n2]['edge_attr']:
							flag = False
							break
					for target in targets1:
						if G[n1][target]['edge_attr']!=G[n2][target]['edge_attr']:
							flag = False
							break
			if flag:
				print 'Nodes', n1, 'and', n2, 'have the same set of neighbors'
				collapse(G,n1,n2)
				toremove+=[n1,n2]
	toremove = set(toremove)
	print toremove
	for rem in toremove:
		print 'Removing node', rem
		G.remove_node(rem)
	return G

#creates a new node that is the merging of two nodes
def collapse(G, n1, n2):
	newn = n1 + '-' + n2
	G.add_node(newn)
	G.node[newn]['label']=newn
	for reg in G.predecessors(n1):
		G.add_edge(reg,newn)
		G[reg][newn]['edge_attr']=G[reg][n1]['edge_attr']
	for target in G.successors(n1):
		G.add_edge(newn,target)
		G[newn][target]['edge_attr']=G[n1][target]['edge_attr']
	#G.remove_node(n1)
	#G.remove_node(n2)
	print 'Collapsed nodes', n1, 'and', n2, 'into', newn
	return G
