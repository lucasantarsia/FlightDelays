from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Connessione:
    V0: Airport
    V1: Airport
    N: int

    def __str__(self):
        return f"{self.V0.ID} - {self.V0.AIRPORT} --- {self.V1.ID} - {self.V1.AIRPORT}"
