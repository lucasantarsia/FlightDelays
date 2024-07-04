import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allAirports = DAO.getAllAirports()
        self._nodi = []
        self._idMap = {}
        for a in self._allAirports:
            self._idMap[a.ID] = a
        self._grafo = nx.Graph()

        self._bestPath = []
        self._bestObjFun = 0

    def buildGraph(self, nMin):
        self._nodi = DAO.getAllNodes(nMin, self._idMap)
        self._grafo.add_nodes_from(self._nodi)
        self._addEdgesV2()

    def _addEdgesV1(self):
        allConnessioni = DAO.getAllEdgesV1(self._idMap)  # queste connessioni hanno delle ripetizioni.
        # Devo controllare quindi che le ripetizione non vengano aggiunte
        for c in allConnessioni:
            v0 = c.V0
            v1 = c.V1
            peso = c.N
            if v0 in self._grafo and v1 in self._grafo:  # se v0 e v1 sono nodi presenti nel grafo
                if self._grafo.has_edge(v0, v1):  # se c'è già l'arco
                    self._grafo[v0][v1]["weight"] += peso
                else:
                    self._grafo.add_edge(v0, v1, weight=peso)

    def _addEdgesV2(self):
        allConnessioni = DAO.getAllEdgesV2(self._idMap)  # queste connessioni NON hanno delle ripetizioni.
        for c in allConnessioni:
            if c.V0 in self._grafo and c.V1 in self._grafo:  # se v0 e v1 sono nodi presenti nel grafo
                self._grafo.add_edge(c.V0, c.V1, weight=c.N)

    def getSortedVicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[v0][v]["weight"]))
        viciniTuple.sort(key=lambda x: x[1], reverse=True)
        return viciniTuple

    def esistePercorso(self, v0, v1):
        connessa = nx.node_connected_component(self._grafo, v0)  # metodo che ritorna la comp connessa che contiene v0
        if v1 in connessa:  # se v1 fa parte della comp connessa vuo dire che esiste un percorso tra v0 e v1
            return True
        return False

    def trovaCamminoD(self, v0, v1):
        return nx.dijkstra_path(self._grafo, v0, v1)  # Dijkstra restituisce il cammino ottimo in termini di peso minore

    def trovaCamminoBFS(self, v0, v1):
        tree = nx.bfs_tree(self._grafo, v0)  # BFS restituisce il cammino più breve in termini di numero di archi
        if v1 in tree:
            print(f"{v1} è presente nell'albero di visita")  # se uso questo metodo posso verificare qui se v1 è connesso a v0
        path = [v1]

        while path[-1] != v0:
            path.append(list(tree.predecessors(path[-1]))[0])  # l' albero ha sempre un predecessore

        path.reverse()  # per avere il path dal source al target
        return path

    def trovaCamminoDFS(self, v0, v1):
        tree = nx.dfs_tree(self._grafo, v0)  # DFS ci restituirà quello più lungo in termini di numero di archi
        if v1 in tree:
            print(
                f"{v1} è presente nell'albero di visita")  # se uso questo metodo posso verificare qui se v1 è connesso a v0
        path = [v1]

        while path[-1] != v0:
            path.append(list(tree.predecessors(path[-1]))[0])  # l' albero ha sempre un predecessore

        path.reverse()  # per avere il path dal source al target
        return path

    def getCamminoOttimo(self, v0, v1, t):
        self._bestPath = []
        self._bestObjFun = 0

        parziale = [v0]  # io cerco un cammino tra v0 e v1, quindi v0 c'è sicuro

        self._ricorsione(parziale, v1, t)

        return self._bestPath, self._bestObjFun

    def _ricorsione(self, parziale, target, t):
        # Verificare che parziale sia una possibile soluzione
            # Verificare che parziale è meglio di best
            # Esco

        if len(parziale) == t+1:
            return

        if self.getObjFun(parziale) > self._bestObjFun and parziale[-1] == target:
            self._bestObjFun = self.getObjFun(parziale)
            self._bestPath = copy.deepcopy(parziale)

        # Posso ancora aggiungere nodi
            # Prendo i vicini e provo ad aggiungere
            # Ricorsione

        for n in self._grafo.neighbors(parziale[-1]):
            # nel caso se ce lo chiede possiamo inserire condizione che non deve passare tra stessi nodi e stessi archi
            if n not in parziale:  # così il percorso non passa dagli stessi nodi
                parziale.append(n)
                self._ricorsione(parziale, target, t)
                parziale.pop()

    def getObjFun(self, listOfNodes):  # ritorna il peso totale dato una lista di nodi
        objVal = 0
        for i in range(0, len(listOfNodes)-1):
            objVal += self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return objVal

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getAllNodes(self):
        return self._nodi

    def printGraphDetails(self):
        print(f"Num nodi: {len(self._grafo.nodes)}")
        print(f"Num archi: {len(self._grafo.edges)}")
