# Yacc example

import ply.yacc as yacc
import networkx as nx

# Get the token map from the lexer.
from tokenizer import tokens
#from tokenizer import tokenize


def new_node(node, network):
	network.add_node(node)
	network.node[node]['label']=node
	return network

class Node():
	
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return "Node %s, color %s, tail %s" % (self.name, self.Color, self.Tail)
	
	#setting default color and edge style
	Color = 'black'
	Tail = 'normal'
	
	#construct an edge from Node to a given target node
	def draw_edge(self,target,G):
		G.add_edge(self.name,target)
		G[self.name][target]['color'] = self.Color
		G[self.name][target]['arrowhead'] = self.Tail
		return G

G = nx.DiGraph()

#invert the color of an edge if it is inhibitory
def colorswap(e,G):
	if G[e[0]][e[1]]['color'] == 'red':
		G[e[0]][e[1]]['color'] = 'blue'
	elif G[e[0]][e[1]]['color'] == 'blue':
		G[e[0]][e[1]]['color'] = 'red'
	return G

def p_rule(p):
	'rule : ID ASSIGN expression'
	new_node(p[1], G)
	p[0] = p[3]
	if isinstance(p[3],Node):
		p[3].draw_edge(p[1],G)
	else:
		for i in list(p[3]):
			i.draw_edge(p[1],G)
	return p

def p_expression_and(p):
	'expression : expression AND term'
	flag = 0 
	if isinstance(p[1],Node):
		p[1].Color = 'blue'
	else:
		flag = 1
		p[1].append(p[3])
	if isinstance(p[3],Node):
		p[3].Color = 'blue'
	if flag:
		p[0] = p[1]
	else:
		p[0] = [p[1],p[3]]
	return p

def p_expression_or(p):
	'expression : expression OR term'
	flag = 0 
	if isinstance(p[1],Node):
		p[1].Color = 'red'
	else:
		flag = 1
		p[1].append(p[3])
	if isinstance(p[3],Node):
		p[3].Color = 'red'
	if flag:
		p[0] = p[1]
	else:
		p[0] = [p[1],p[3]]
	return p

def p_expression_term(p):
	'expression : term'
	p[0] = p[1]
	return p

def p_term_not(p):
	'term : NOT term'
	if isinstance(p[2],Node):
		p[2].Tail = 'tee'
	p[0] = p[2]
	return p

def p_term(p):
	'term : ID'
	p[0] = Node(p[1])
	new_node(p[1], G)
	return p

def p_term_expr(p):
	'term : LPAREN expression RPAREN'
	fakenode =''
	for i in p[2]:
		fakenode +=(i.name+'-')
	new_node(fakenode, G)
	for i in p[2]:
		i.draw_edge(fakenode,G)
	p[0] = Node(fakenode)
	return p

# Error rule for syntax errors
def p_error(p):
	print "Syntax error in input!"


# Build the parser
parser = yacc.yacc()

#Read from file
ifile = '/home/parul/Dropbox/codes/rules/forply/main.txt'
f = open(ifile, 'r')
text = f.read()
text_iter = iter(text.splitlines())

#run the parser for each line in the file
for s in text_iter:
	edges = {}
	parser.parse(s)

#invert the color of inhibitory edges
for e in G.edges_iter(data=True):
	if G[e[0]][e[1]]['arrowhead'] == 'tee':
		colorswap(e,G)

#Write to a graph
gfile = '/home/parul/Dropbox/codes/EMT_complt/byply/main.graphml'
nx.write_graphml(G,gfile)

print 'Graph created at', gfile