from datetime import datetime

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

print("Metodo di Dijkstra")  # Dijkstra restituisce il cammino ottimo in termini di peso minore
print(*pathD, sep='\n')
print("------")
print("Metodo albero Breadth first")  # BFS restituisce il cammino più breve in termini di numero di archi
print(*pathBFS, sep='\n')
print("------")
print("Metodo albero Depth first")  # DFS ci restituirà quello più lungo in termini di numero di archi
print(*pathDFS, sep='\n')

tic = datetime.now()
bestPath, bestScore = mymodel.getCamminoOttimo(v0, v1, 4)
print("-----------------")
print(f"Cammino ottimo da {v0} a {v1} ha peso: {bestScore}.\n Trovato in {datetime.now() - tic}")
print(*bestPath, sep='\n')
