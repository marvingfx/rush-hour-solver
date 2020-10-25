from dataclasses import dataclass
import numpy as np
from typing import Tuple, Iterator, List


@dataclass(frozen=True)
class Board:
    width: int
    vehicles: Tuple["Vehicle"]

    def move_vehicle(self, move: "Move") -> "Board":
        vehicles = self.vehicles[0: move.vehicle_index] + (
            self.vehicles[move.vehicle_index].move(move),) + self.vehicles[move.vehicle_index + 1:]
        return Board(self.width, vehicles)

    @staticmethod
    def from_matrix(matrix: List[List[int]]) -> "Board":
        if len(matrix) < 6 or len(matrix) is not len(matrix[0]):
            raise Exception('Wrong shape for matrix. Matrices should be square and have at least 6 rows and columns')
        else:
            symbol_dict = dict()

            for row_index, row in enumerate(matrix):
                for column_index, column in enumerate(row):
                    if column not in symbol_dict:
                        symbol_dict[column] = [(row_index, column_index)]
                    else:
                        symbol_dict[column].append((row_index, column_index))

            vehicles = tuple(Vehicle(vehicle_id, tuple(positions), positions[0][0] == positions[-1][0]) for
                             vehicle_id, positions in
                             symbol_dict.items() if not vehicle_id == -1)

            return Board(len(matrix), vehicles)

    def is_final_configuration(self) -> bool:
        red_vehicle = next(vehicle for vehicle in self.vehicles if vehicle.id == 0)
        return red_vehicle.positions[-1][1] == self.width - 1

    def get_moves(self) -> Iterator["Move"]:
        for index, vehicle in enumerate(self.vehicles):
            backward_position = None
            forward_position = None

            if vehicle.horizontal:
                if vehicle.positions[0][1] > 0:
                    backward_position = (vehicle.positions[0][0], vehicle.positions[0][1] - 1)
                if vehicle.positions[-1][1] < self.width - 1:
                    forward_position = (vehicle.positions[-1][0], vehicle.positions[-1][1] + 1)

            else:
                if vehicle.positions[0][0] > 0:
                    backward_position = (vehicle.positions[0][0] - 1, vehicle.positions[0][1])
                if vehicle.positions[-1][0] < self.width - 1:
                    forward_position = (vehicle.positions[-1][0] + 1, vehicle.positions[-1][1])

            for other_vehicle in self.vehicles:
                if forward_position in other_vehicle.positions:
                    forward_position = None
                if backward_position in other_vehicle.positions:
                    backward_position = None

            if forward_position is not None:
                yield Move(vehicle_id=vehicle.id, vehicle_index=index, move=1)
            if backward_position is not None:
                yield Move(vehicle_id=vehicle.id, vehicle_index=index, move=-1)

    def __repr__(self):
        matrix = np.full(shape=(self.width, self.width), fill_value=-1)
        for vehicle in self.vehicles:
            for position in vehicle.positions:
                matrix[position[0]][position[1]] = vehicle.id
        return str(matrix)

    def __hash__(self):
        return hash(self.vehicles)


@dataclass(frozen=True)
class Vehicle:
    id: int
    positions: Tuple[Tuple[int, int]]
    horizontal: bool

    def move(self, move: "Move") -> "Vehicle":
        positions = tuple(
            map(lambda x: (x[0], x[1] + move.move) if self.horizontal else (x[0] + move.move, x[1]), self.positions))
        return Vehicle(self.id, positions, self.horizontal)


@dataclass(frozen=True)
class Move:
    vehicle_id: int = -1
    vehicle_index: int = -1
    move: int = 0
