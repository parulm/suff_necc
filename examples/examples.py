import sys
sys.path.append('../')

import networkx as nx
import boolparser
import gprops
import subgraph

def toyExample():
	rulefile = 'toy_rules.txt'
	G = boolparser.readfile(rulefile)
	gprops.set_edge_type(G)
	signals = ['S1', 'S2']
	outputs = ['O']
	
	#show the major subgraph and motif types
	print subgraph.finalsg(G, 'S1', 'B')
	print subgraph.finalsg(G, 'S2', 'F')
	print subgraph.finalsg(G, 'C', 'C', motif=True)
	print subgraph.finalsg(G, 'F', 'F', motif=True)
	print subgraph.finalsg(G, 'F', 'O')

	#general way of finding all motifs of the network
	motifnodes = []
	print 'Listing the nodes that are a part of a motif'
	for node in G.nodes():
		#Setting seen as empty ensures that the code explores the entire network for possible pathways.
		motiftype = subgraph.finalsg(G, node, node, seen=[], motif=True)
		if motiftype is not None:
			print 'motif', motiftype, 'at node', node
			motifnodes.append(node)

	#finding subgraphs from signals to motif nodes in the network, excluting output nodes
	print 'Listing the types of subgraphs from the signals to the motif nodes'
	for s in signals:
		for node in motifnodes:
			sgtype = subgraph.finalsg(G, s, node, seen=[])
			if sgtype is not None:
				print sgtype, 'subgraph found from', s, 'to', node


	#finding subgraphs from motifs to output
	print 'Listing the types of subgraphs from the motif nodes to the output node'
	for node in motifnodes:
		for o in outputs:
			outsgtype = subgraph.finalsg(G, node, o, seen=[])
			if outsgtype is not None:
				print outsgtype, 'subgraph found from', node, 'to', o

	return None

def EMTexample():
	rulefile = 'EMT_rules.txt'
	G = boolparser.readfile(rulefile)
	gprops.set_edge_type(G)
	signals = ['SHH','Wnt','HGF','PDGF','IGF1','EGF','FGF','Jagged','TGFb','DELTA','CHD1L','Goosecoid','Hypoxia']
	outputs = ['EMT']

	#find all nodes in the motifs
	print 'Listing the nodes that are a part of a motif'
	motifnodes = []
	for node in G.nodes():
		motiftype = subgraph.finalsg(G, node, node, seen=[], motif=True)
		if motiftype is not None:
			print 'motif', motiftype, 'at node', node
			motifnodes.append(node)

	#find subgraphs from the signal nodes to the motifs
	print 'Listing the types of subgraphs from the signals to the motif nodes'
	for s in signals:
		for mnode in motifnodes:
			sgtype = subgraph.finalsg(G, s, mnode, seen=[])
			if sgtype is not None:
				print sgtype, 'subgraph found from', s, 'to', mnode
	
	#find subgraphs from the motifnodes to the output node
	print 'Listing the types of subgraphs from the motif nodes to the output node'
	for mnode in motifnodes:
		for o in outputs:
			outsgtype = subgraph.finalsg(G, mnode, o, seen=[])
			if outsgtype is not None:
				print outsgtype, 'subgraph from', mnode, 'to', o

	return None


if __name__ == '__main__':
	print 'Analyzing the toy example'
	toyExample()
	print '\nAnalyzing the EMT network'
	EMTexample()