from database.DB_connect import DBConnect
from model.artist import Artist
from model.edge import Edge


class DAO():
    def __init__(self):
        pass

    def getArtists(self, genreId: int) -> [Artist]:
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select ar.ArtistId as artistId, ar.Name as name, coalesce(sum(i.Quantity), 0) as popularity
                    from artist ar, album al, track t left join invoiceline i on t.TrackId = i.TrackId
                    where ar.ArtistId = al.ArtistId and t.AlbumId = al.AlbumId and t.GenreId = %s
                    group by ar.ArtistId"""

        cursor.execute(query, (genreId,))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    def getEdges(self, genreId: int) -> [Edge]:
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select ar1.ArtistId as a1, ar2.ArtistId as a2
                    from artist ar1, album al1, track t1, invoiceline il1, invoice i1,
                    artist ar2, album al2, track t2, invoiceline il2, invoice i2
                    where ar1.ArtistId = al1.ArtistId and t1.AlbumId = al1.AlbumId and t1.TrackId = il1.TrackId
                    and il1.InvoiceId = i1.InvoiceId and t1.GenreId = %s
                    and ar2.ArtistId = al2.ArtistId and t2.AlbumId = al2.AlbumId and t2.TrackId = il2.TrackId
                    and il2.InvoiceId = i2.InvoiceId and t2.GenreId = %s
                    and ar1.ArtistId < ar2.ArtistId and i1.CustomerId = i2.CustomerId"""

        cursor.execute(query, (genreId, genreId))

        for row in cursor:
            result.append(Edge(**row))

        cursor.close()
        conn.close()
        return result

    def getAllGenres(self) -> [str]:
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select GenreId, Name
                    from genre"""

        cursor.execute(query,)

        for row in cursor:
            result.append((row["GenreId"], row["Name"]))

        cursor.close()
        conn.close()
        return result

