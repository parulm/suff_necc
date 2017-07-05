## Library to analyze boolean networks in causal logic framework.
### Details of all the functions
#### boolparser.readfile:
Constructs the causal logic representation of a network from Boolean rules. Assigns color and edge (tail) type to a regulator on the basis of the Boolean rule.
#### gprops.set_edge_type:
Setting the edge attribute so that every time we do not have to read and combine both color and arrowhead type. This function reads a graph and sets a new edge attribute named edge_attr to s/n, s/ni, s, n, si or ni.
#### gprops.set_edge_props:
Sets color and arrowhead type on the basis of the edge attribute edge_attr.
#### gprops.node_type:
Takes a graph and it's node and returns the node type. Node type is red if its' regulators are related by OR rule, blue if AND rule and black if the node takes a single regulator.
#### gprops.lone_reg:
Takes a graph and sets all single regulator nodes' edges as s/n or s/ni depending on what the original edge was.
#### path.add:
Adds two types of relationships. The order is important here, preceding type is relationship while the succeeding one is edge_type.
#### path.path_type:
Takes a graph and a list of nodes, path, which form a path in the graph. This function sequentially adds all the edges in the path and returns the type of the entire path.
#### reduction.edge_red:
Logical transitive reduction: Takes a graph and deletes every edge for which a path exists that causes the same effect as the edge.
#### reduction.node_collapse:
Collapses all sufficient-necessary and sufficient-necessary inhibitory edges in a network.
#### subgraph.finalsg:
Finds subgraph in a given graph between specified source and target nodes.
