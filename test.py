import importlib
import networkx as nx

fname = ''
G = nx.DiGraph()

G = importlib.read_boolean(fname)

nx.write_graphml(G,'')