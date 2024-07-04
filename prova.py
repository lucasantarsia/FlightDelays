import copy

import networkx as nx

class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()

        self.bestPath = []
        self.bestObjFun = 0


    def buildGraph(self):
        self.grafo.add_edge(1, 2, weight=1)
        self.grafo.add_edge(2, 3, weight=2)
        self.grafo.add_edge(3, 4, weight=3)
        self.grafo.add_edge(2, 5, weight=4)
        self.grafo.add_edge(5, 6, weight=5)
        self.grafo.add_edge(6, 7, weight=6)
        self.grafo.add_edge(6, 8, weight=7)
        self.grafo.add_edge(4, 7, weight=50)
        self.grafo.add_edge(8, 7, weight=50)


    """Modo per trovare la componente connessa di un nodo"""
    def getConnessa(self):
        connessa = list(nx.node_connected_component(self.grafo, 2))
        print(f"Componente connessa al nodo 2: {connessa}")
        print("------")


    """Modo per trovare tutte le componenti connesse presenti nel grafo"""
    def getCompConnesse(self):
        connesse = list(nx.connected_components(self.grafo))
        print("Tutte le componenti connesse:")
        for connessa in connesse:
            print(list(connessa))
        print("------")


    """Modo per trovare il cammino con peso totale minimo (Dijkstra)"""
    def getCamminoDijkstra(self):
        camminoMinimo = nx.dijkstra_path(self.grafo, 2, 7)
        print(f"Cammino da 4 a 7 con peso totale minimo (Dijkstra): {camminoMinimo}")

        # oppure

        dist, path = nx.single_source_dijkstra(self.grafo, 2, 7)
        print(f"{dist} -- {path}")
        print("------")


    """Modo per trovare il cammino più breve (BFS)"""
    def getCamminoBFS(self):
        tree = nx.bfs_tree(self.grafo, 2)
        if 7 in tree:
            print(f"7 è presente nell'albero di visita")
        path = [7]
        while path[-1] != 2:
            path.append(list(tree.predecessors(path[-1]))[0])
        path.reverse()
        print(f"Cammino da 4 a 7 più breve (BFS): {path}")

        print("------")


    """Modo per trovare il cammino più lungo (DFS)"""
    def getCamminoDFS(self):
        tree = nx.dfs_tree(self.grafo, 2)
        if 7 in tree:
            print(f"7 è presente nell'albero di visita")
        path = [7]
        while path[-1] != 2:
            path.append(list(tree.predecessors(path[-1]))[0])
        path.reverse()
        print(f"Cammino da 4 a 7 più lungo (DFS): {path}")

        print("------")


    """Algoritmo ricorsivo per cercare un percorso tra un nodo n e un nodo target
    tale per cui massimizzi la somma dei pesi degli archi attraversati, utilizzando
    al massimo un numero archiMax di archi"""
    def getBestPath(self, n, target, archiMax):
        self.bestPath = []
        self.bestObjFun = 0
        parziale = [n]  # io cerco un cammino tra n e target, quindi n c'è sicuro

        self.ricorsione(parziale, target, archiMax)

        return self.bestPath, self.bestObjFun


    def ricorsione(self, parziale, target, archiMax):
        # Verificare che parziale sia una possibile soluzione
        if len(parziale) == archiMax + 1:
            return

        # Verificare che parziale è meglio di best
        if self.getObjFun(parziale) > self.bestObjFun and parziale[-1] == target:
            self.bestObjFun = self.getObjFun(parziale)
            self.bestPath = copy.deepcopy(parziale)

        # Posso ancora aggiungere nodi
        for n in self.grafo.neighbors(parziale[-1]):
            # qui possiamo inserire altre eventuali condizione:
            if n not in parziale:  # così il percorso non passa dagli stessi nodi
                parziale.append(n)
                self.ricorsione(parziale, target, archiMax)
                parziale.pop()

    def getObjFun(self, listOfNodes):  # ritorna il peso totale dato una lista di nodi
        objVal = 0
        for i in range(0, len(listOfNodes) - 1):
            objVal += self.grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return objVal


if __name__ == '__main__':
    model = Model()

    model.buildGraph()
    print(f"nodi: {model.grafo.nodes}")
    print(f"archi: {model.grafo.edges}")
    print("------")

    #model.getConnessa()

    #model.getCompConnesse()

    model.getCamminoDijkstra()

    model.getCamminoBFS()

    model.getCamminoDFS()

    bestPath, pesoTot = model.getBestPath(2, 7, 3)
    print(f"Percorso da 2 a 7 con peso totale massimo e che passa per massimo 3 archi "
          f"ha peso = {pesoTot} e passa per i seguenti nodi:")
    print(bestPath)
    for n in bestPath:
        print(n)

    print("------")

    """Successori del nodo 2"""
    successori = list(nx.bfs_successors(model.grafo, 2, depth_limit=1))
    print(successori[0][1])


    successori = list(nx.dfs_successors(model.grafo, 2, depth_limit=2))
    print(successori)

    predecessori = list(nx.bfs_predecessors(model.grafo, 2, depth_limit=1))
    print(predecessori)

    predecessori = list(nx.dfs_predecessors(model.grafo, 2, depth_limit=1))
    print(predecessori)


    """Predecessori del nodo 7"""
    mieiPred = []
    for n1, n2 in model.grafo.edges:
        if n2 == 7:
            mieiPred.append(n1)
    print(mieiPred)


    """Nodi raggiungibili da un nodo dato"""
    connessa = list(nx.bfs_tree(model.grafo, 2))
    print(connessa[1:])


    print("RICOMINCIAMO...")


    successori = list(model.grafo.successors(6))
    print(successori)

    predecessori = list(model.grafo.predecessors(2))
    print(predecessori)


    print(model.grafo.has_successor(2, 6))

