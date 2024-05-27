import networkx as nx

from database.DAO import DAO
from model.model import Model

mymodel = Model()
mymodel.buildGraph(5)
mymodel.printGraphDetails()

v0 = mymodel.getAllNodes()[0]

connessa = list(nx.node_connected_component(mymodel._grafo, v0))
v1 = connessa[10]

pathD = mymodel.trovaCamminoD(v0, v1)
pathBFS = mymodel.trovaCamminoBFS(v0, v1)
pathDFS = mymodel.trovaCamminoDFS(v0, v1)

print("Metodo di Dijkstra")  # Dijkstra restutisce il cammino piu breve e con gli archi con peso minore
print(*pathD, sep='\n')
print("------")
print("Metodo albero Breadth first")
print(*pathBFS, sep='\n')
print("------")
print("Metodo albero Depth first")  # DFS ci restituirà quello più lungo
print(*pathDFS, sep='\n')
