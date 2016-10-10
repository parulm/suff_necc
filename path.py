#collection of path functions

import networkx as nx

#Adds two types of relationships. The order is important here, preceding type is relationship while the succeeding one is edge_type. All not-addable pairs return null which can be used to check for subgraphs.
def add(relationship,edge_type):
    if relationship=='s/n':
        return edge_type
    
    elif edge_type=='s/n':
        return relationship
    
    elif relationship=='s':
        if edge_type=='s':
            return 's'
        elif edge_type=='si':
            return 'si'
        elif edge_type=='s/ni':
            return 'si'
        else:
            return 'null'
    
    elif relationship=='n':
        if edge_type=='n':
            return 'n'
        elif edge_type=='ni':
            return 'ni'
        elif edge_type=='s/ni':
            return 'ni'
        else:
            return 'null'
    
    elif relationship=='si':
        if edge_type=='n':
            return 'si'
        elif edge_type=='ni':
            return 's'
        elif edge_type=='s/ni':
            return 's'
        else:
            return 'null'
    
    elif relationship=='ni':
        if edge_type=='s':
            return 'ni'
        elif edge_type=='si':
            return 'n'
        elif edge_type=='s/ni':
            return 'n'
        else:
            return 'null'
        
    elif relationship=='s/ni':
        if edge_type=='s':
            return 'si'
        elif edge_type=='n':
            return 'ni'
        elif edge_type=='si':
            return 'n'
        elif edge_type=='ni':
            return 's'
        elif edge_type=='s/ni':
            return 's/n'
        else:
            return 'null'

#Takes a graph and a list of nodes, path, which form a path in the graph. The function does not check if the given list is actually a path, if not it might throw in an ugly error. This function sequentially adds all the edges in the path and returns the total effect of the entire path and hence reflects the relationship between the first and last nodes of the list passed.
#Possible fix: Can add a has_edge function at every iteration.
def path_type(G, path):
    l = len(path)
    relationship = 's/n'
    for i in range(l-1):
        u = path[i]
        v = path[i+1]
        edge_type = G[u][v]['edge_attr']
        new_rel = add(relationship,edge_type)
        if new_rel=='null':
            return 'nothing'
        else:
            relationship = new_rel
    return relationship

