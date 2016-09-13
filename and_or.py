#This code plots a sufficient-necessary representation of a network from an input file listing the update rules
#Fixes needed; reads extra space as a node
#Major bug fixes needed - cannot cancel consecutive NOTs; doesn't eliminate unnecessary brackets; fails on nested brackets; check the entire graph for homogeneity rule once it is constructed - assign node colors; produce reduced network if initial values of some variables is given

import networkx as nx
import matplotlib.pyplot as plt
import graphviz
import pydot
import sys

rulefile = sys.argv[1]

G = nx.DiGraph()

def create_node(node,node_list):
  G.add_node(node)
  G.node[node]['label']=node
  #add node and knowledge of its update function in array node_list
  node_list[0].append(node)
  node_list[1].append(0)
  return True

keywds = ['NOT','not','AND','and','OR','or']

infile = rulefile + '.txt'
f = open(infile,'r+')

#f.seek(0)
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
      create_node(node,node_list)
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
        create_node(str(comp),node_list)
        cnode = str(comp)
        words[j] = words[j][1:]
        end_found = False
      if words[j] not in keywds:
        #this must be a node, add it to the list if it's not there
        if words[j] not in node_list[0]:
          create_node(words[j],node_list)
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
  #print (words)

#Uncomment the following code to see the network drawn by matplotlib - cannot differentiate between negative and positive edges
#colors = [G[u][v]['color'] for u,v in G.edges()]
#nx.draw(G, with_labels = True, arrows = True, edge_color=colors)
#plt.show()

outgraphml = rulefile + '.graphml'
nx.write_graphml(G,outgraphml)
outdot = rulefile + '.dot'
outpng = rulefile + '.png'
nx.drawing.nx_agraph.write_dot(G,outdot)
graph = nx.drawing.nx_pydot.to_pydot(G)
graph.write_png(outpng)