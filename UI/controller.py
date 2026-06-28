import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genres = self._model.getAllGenres()
        for genre in genres:
            genreName = genre[1]
            self._view._ddGenre.options.append(ft.dropdown.Option(data=genreName, key=genreName))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        genre = self._view._ddGenre.value
        if genre is None:
            self._view.txt_result.controls.append(ft.Text("Errore! Selezionare un valore.", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(genre)
        mostInfluentArtist = self._model.getMostInfluentArtist()
        topFiveEdgesText = "\n".join(f"{a1} -> {a2}: {data["weight"]}" for a1, a2, data in self._model.getTopFiveEdges())
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {len(self._model._graph.nodes)}\n"
                                                      f"Numero archi: {len(self._model._graph.edges)}\n"
                                                      f"Artista più influente: {mostInfluentArtist[0]} con influenza {mostInfluentArtist[1]}\n"
                                                      f"Top 5 archi:\n{topFiveEdgesText}"))
        self._view.update_page()


    def handleCammino(self,e):
        pass