from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._aeroportoP = None
        self._aeroportoA = None

    def handleAnalizza(self, e):
        self._view._txt_result.controls.clear()
        nMin_str = self._view._txtInNumC.value
        try:
            nMin = int(nMin_str)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Il valore inserito nel campo nMin non è un intero."))
            self._view.update_page()
            return
        self._model.buildGraph(nMin)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(ft.Text(f"Num nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(ft.Text(f"Num archi: {self._model.getNumArchi()}"))

        self._view._ddAeroportoP.disabled = False
        self._view._ddAeroportoA.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._btnPercorso.disabled = False

        self.fillDD()
        self._view.update_page()

    def handleConnessi(self, e):
        if self._aeroportoP is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare un aeroporto di partenza."))
            self._view.update_page()
            return
        v0 = self._aeroportoP
        vicini = self._model.getSortedVicini(v0)
        self._view._txt_result.controls.append(ft.Text(f"Ecco i vicini di {v0}:"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    def handleTestConnessione(self, e):
        v0 = self._aeroportoP
        v1 = self._aeroportoA

        self._view._txt_result.controls.clear()

        # verificare che ci sia un percorso
        if (not self._model.esistePercorso(v0, v1)):
            self._view._txt_result.controls.append(ft.Text(f"Non esiste un percorso fra {v0} e {v1}."))
            self._view.update_page()
            return
        else:
            self._view._txt_result.controls.append(ft.Text(f"Percorso fra {v0} e {v1} trovato."))
            self._view.update_page()

        path = self._model.trovaCamminoBFS(v0, v1)
        self._view._txt_result.controls.append(ft.Text(f"Il cammino con minor numero di archi tra {v0} e {v1} è:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))

        self._view._txtInNumTratte.disabled = False
        self._view._btnCercaItinerario.disabled = False
        self._view.update_page()

        # trovare un possibile percorso

    def handleCercaItinerario(self, e):
        v0 = self._aeroportoP
        v1 = self._aeroportoA
        t = self._view._txtInNumTratte.value

        try:
            tInt = int(t)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Il valore inserito non è un numero"))
            self._view.update_page()
            return

        tic = datetime.now()
        path, nTot = self._model.getCamminoOttimo(v0, v1, tInt)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il percorso ottimo tra {v0} e {v1} è:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(p))
        self._view._txt_result.controls.append(ft.Text(f"Numero totale di voli: {nTot}"))
        self._view._txt_result.controls.append(ft.Text(f"Tempo impiegato per la ricerca: {datetime.now()-tic} secondi"))
        self._view.update_page()

    def fillDD(self):
        for n in self._model.getAllNodes():
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(text=n.AIRPORT,
                                                                       data=n,
                                                                       on_click=self.read_ddAeroportoP))
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(text=n.AIRPORT,
                                                                       data=n,
                                                                       on_click=self.read_ddAeroportoA))

    def read_ddAeroportoP(self, e):
        if e.control.data is None:
            self._aeroportoP = None
        else:
            self._aeroportoP = e.control.data
        print(f"read_ddAeroportoP called: {self._aeroportoP}")

    def read_ddAeroportoA(self, e):
        if e.control.data is None:
            self._aeroportoA = None
        else:
            self._aeroportoA = e.control.data
        print(f"read_ddAeroportoA called: {self._aeroportoA}")
