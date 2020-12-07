from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    vehicle_id: int = -1
    vehicle_index: int = -1
    move: int = 0
