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
        pass

    def handleCercaItinerario(self, e):
        pass

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
