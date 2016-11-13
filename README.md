##Library to handle boolean networks in sufficient-necessary framework.
###Details of all the functions
####importlib.gml2dot:
Takes a gml file in updated format and returns a networkx graph with only the needed edge and node properties.
####importlib.read_boolean:
Reads a set of Boolean rules and returns the graph with suitable edge properties. f<sub>A</sub> = B and C must be represented as A* = B and C. A combination of AND & OR rules must be neatly packed in brackets. Extra spaces and brackets cause the code to break. 
####gprops.importgraph:
Returns a graph neatly read from a gml file in the updated format.
####gprops.set_edge_type:
Setting the edge attribute so that every time we do not have to read and combine both color and arrowhead type. This function reads a graph and sets a new edge attribute named edge_attr to s/n, s/ni, s, n, si or ni.
####gprops.node_homog:
Takes a graph and a node of the graph, returns True if homogeneity is being satisfied at the node, else returns False.
####gprops.set_edge_props:
Sets color and arrowhead type on the basis of the edge attribute edge_attr.
####gprops.node_type:
Takes a graph and it's node and returns the node type. Node type is red if its' regulators are related by OR rule, blue if AND rule and black if the node takes a single regulator.
####gprops.lone_reg:
Takes a graph and sets all single regulator nodes' edges as s/n or s/ni depending on what the original edge was.
####path.add:
Adds two types of relationships. The order is important here, preceding type is relationship while the succeeding one is edge_type.
####path.path_type:
Takes a graph and a list of nodes, path, which form a path in the graph. This function sequentially adds all the edges in the path and returns the type of the entire path.
####reduction.edge_red:
Logical transitive reduction: Takes a graph and deletes every edge for which a path exists that causes the same effect as the edge.
####reduction.pnode_collapse:
Takes a graph and collapses pseudo nodes where either the incoming or outgoing edge is singular and s/n.
####reduction.homog_pnode:
Takes a graph and for every pseudo node with only one outgoing edge which is of the same type as the incoming ones, the node is collapsed.