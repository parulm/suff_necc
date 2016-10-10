#collection of path functions

import networkx as nx

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

