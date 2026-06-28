import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._dao = DAO()
        self._idMapGenre = {}
        for id, name in self._dao.getAllGenres():
            self._idMapGenre[name] = id
        self._idMapArtist = {}

    def buildGraph(self, selectedGenre: str):
        self._graph.clear()
        artists = self.getArtists(selectedGenre)
        self._graph.add_nodes_from(artists)
        self.addEdges(selectedGenre)


    def getArtists(self, selectedGenre):
        genreId = self._idMapGenre[selectedGenre]
        artists = self._dao.getArtists(genreId)
        for a in artists:
            self._idMapArtist[a.artistId] = a
        return artists

    def addEdges(self, selectedGenre):
        genreId = self._idMapGenre[selectedGenre]
        artistsEdges = self._dao.getEdges(genreId)
        for e in artistsEdges:
            a1 = self._idMapArtist[e.a1]
            a2 = self._idMapArtist[e.a2]
            if a1.popularity > a2.popularity:
                self._graph.add_edge(a1, a2, weight = a1.popularity + a2.popularity)
            elif a1.popularity < a2.popularity:
                self._graph.add_edge(a2, a1, weight = a2.popularity + a1.popularity)
            else:
                self._graph.add_edge(a1, a2, weight = a1.popularity + a2.popularity)
                self._graph.add_edge(a2, a1, weight = a2.popularity + a1.popularity)

    def getAllGenres(self):
        return self._dao.getAllGenres()

    def getMostInfluentArtist(self):
        allArtistsInfluence = []
        for a in self._graph.nodes:
            influence = 0
            for e in self._graph.edges(data=True):
                if e[0] == a:
                    influence += e[2]["weight"]
                elif e[1] == a:
                    influence -= e[2]["weight"]
            allArtistsInfluence.append((a, influence))
        allArtistsInfluence.sort(key=lambda x: x[1], reverse=True)
        return allArtistsInfluence[0]

    def getTopFiveEdges(self):
        topFiveEdges = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)
        return topFiveEdges[:5]