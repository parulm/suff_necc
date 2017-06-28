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
	for edge in G.edges():
		u = edge[0]
		v = edge[1]
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