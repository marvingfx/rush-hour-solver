from csv import reader
from dataclasses import dataclass, replace
from typing import Iterator, List, Tuple

from ..model.move import Move
from ..model.vehicle import Vehicle


@dataclass(frozen=True)
class Board:
    width: int
    vehicles: Tuple[Vehicle]

    def move_vehicle(self, move: Move) -> "Board":
        vehicles = (
            self.vehicles[0 : move.vehicle_index]
            + (self.vehicles[move.vehicle_index].move(move),)
            + self.vehicles[move.vehicle_index + 1 :]
        )
        return replace(self, vehicles=vehicles)

    @staticmethod
    def from_matrix(matrix: List[List[int]]) -> "Board":
        if len(matrix) < 6 or len(matrix) is not len(matrix[0]):
            raise Exception(
                "Wrong shape for matrix. Matrices should be square and have at least 6 rows and columns"
            )
        else:
            symbol_dict = dict()

            for row_index, row in enumerate(matrix):
                for column_index, column in enumerate(row):
                    if column not in symbol_dict:
                        symbol_dict[column] = [(row_index, column_index)]
                    else:
                        symbol_dict[column].append((row_index, column_index))

            vehicles = tuple(
                Vehicle(
                    id=vehicle_id,
                    tiles=tuple(tiles),
                    horizontal=tiles[0][0] == tiles[-1][0],
                )
                for vehicle_id, tiles in sorted(symbol_dict.items())
                if vehicle_id >= 0
            )

            return Board(len(matrix), vehicles=vehicles)

    @staticmethod
    def from_csv(file_path: str) -> "Board":
        with open(file_path, "r") as csv_file:
            csv_reader = reader(csv_file)
            matrix = [[int(tile) for tile in line] for line in csv_reader]
            return Board.from_matrix(matrix)

    def is_final_configuration(self) -> bool:
        return self.vehicles[0].tiles[-1][1] == self.width - 1

    def get_minimum_cost(self) -> int:
        return (
            len(self.get_tiles_to_cover_by_red())
            + self.minimum_steps_required_to_clear_direct_path()
        )

    def minimum_steps_required_to_clear_direct_path(self) -> int:
        tiles = self.get_tiles_to_cover_by_red()
        minimum_steps = 0

        for vehicle in self.vehicles_in_the_way_of_red():
            if len(vehicle.tiles) < 2:
                minimum_steps += 1
            else:
                for tile in tiles:
                    try:
                        index_of_tile = vehicle.tiles.index(tile)
                        minimum_steps += min(
                            index_of_tile + 1,
                            len(vehicle.tiles) - index_of_tile,
                        )
                        continue
                    except ValueError:
                        continue

        return minimum_steps

    def vehicles_in_the_way_of_red(self) -> Iterator[Vehicle]:
        tiles = self.get_tiles_to_cover_by_red()

        for vehicle in self.vehicles:
            if any(tile for tile in tiles if tile in vehicle.tiles):
                yield vehicle

    def get_tiles_to_cover_by_red(self):
        return [
            (self.vehicles[0].tiles[-1][0], pos)
            for pos in range(self.vehicles[0].tiles[-1][1] + 1, self.width)
        ]

    def get_moves(self) -> Iterator[Move]:
        for index, vehicle in enumerate(self.vehicles):
            backward_tile = None
            forward_tile = None
            horizontal_move = 1 if vehicle.horizontal else 0
            vertical_move = abs(horizontal_move - 1)

            if vehicle.tiles[0][horizontal_move] > 0:
                backward_tile = (
                    vehicle.tiles[0][0] - vertical_move,
                    vehicle.tiles[0][1] - horizontal_move,
                )
            if vehicle.tiles[-1][horizontal_move] < self.width - 1:
                forward_tile = (
                    vehicle.tiles[-1][0] + vertical_move,
                    vehicle.tiles[-1][1] + horizontal_move,
                )

            for other_vehicle in self.vehicles:
                if forward_tile in other_vehicle.tiles:
                    forward_tile = None
                if backward_tile in other_vehicle.tiles:
                    backward_tile = None

            if forward_tile is not None:
                yield Move(vehicle_id=vehicle.id, vehicle_index=index, move=1)
            if backward_tile is not None:
                yield Move(vehicle_id=vehicle.id, vehicle_index=index, move=-1)

    def __repr__(self):
        matrix = [[-1 for _ in range(self.width)] for _ in range(self.width)]
        for vehicle in self.vehicles:
            for tile in vehicle.tiles:
                matrix[tile[0]][tile[1]] = vehicle.id
        return str(matrix)

    def __hash__(self):
        return hash(self.vehicles)
