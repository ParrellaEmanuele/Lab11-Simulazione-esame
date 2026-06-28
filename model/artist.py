from dataclasses import dataclass


@dataclass
class Artist:
    artistId: int
    name: str
    popularity: int

    def __hash__(self):
        return hash(self.artistId)

    def __eq__(self, other):
        return self.artistId == other.artistId

    def __str__(self):
        return self.name