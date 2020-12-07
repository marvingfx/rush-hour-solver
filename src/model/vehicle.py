from dataclasses import dataclass
from typing import Tuple

from ..model.move import Move


@dataclass(frozen=True)
class Vehicle:
    id: int
    tiles: Tuple[Tuple[int, int]]
    horizontal: bool

    def move(self, move: Move) -> "Vehicle":
        tiles = tuple(
            map(
                lambda x: (x[0], x[1] + move.move)
                if self.horizontal
                else (x[0] + move.move, x[1]),
                self.tiles,
            )
        )
        return Vehicle(id=self.id, tiles=tiles, horizontal=self.horizontal)
