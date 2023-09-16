from src.model import Board, Vehicle, csv_to_matrix
import pytest


def test_csv_to_matrix():
    matrix = csv_to_matrix("boards/board1.csv")
    assert [
        [-1, -1, 1, 2, 2, 3],
        [-1, -1, 1, -1, -1, 3],
        [-1, -1, 1, 0, 0, 3],
        [-1, -1, -1, 4, 5, 5],
        [6, 7, 7, 4, -1, -1],
        [6, -1, -1, 4, 8, 8],
    ] == matrix


def test_create_board_from_csv():
    board = Board.from_csv("boards/board1.csv")
    assert board.width == 6
    assert board.vehicles == (
        Vehicle(id=0, tiles=((2, 3), (2, 4)), horizontal=True),
        Vehicle(id=1, tiles=((0, 2), (1, 2), (2, 2)), horizontal=False),
        Vehicle(id=2, tiles=((0, 3), (0, 4)), horizontal=True),
        Vehicle(id=3, tiles=((0, 5), (1, 5), (2, 5)), horizontal=False),
        Vehicle(id=4, tiles=((3, 3), (4, 3), (5, 3)), horizontal=False),
        Vehicle(id=5, tiles=((3, 4), (3, 5)), horizontal=True),
        Vehicle(id=6, tiles=((4, 0), (5, 0)), horizontal=False),
        Vehicle(id=7, tiles=((4, 1), (4, 2)), horizontal=True),
        Vehicle(id=8, tiles=((5, 4), (5, 5)), horizontal=True),
    )


def test_create_board_from_matrix():
    board = Board.from_matrix(
        [
            [-1, -1, 1, 2, 2, 3],
            [-1, -1, 1, -1, -1, 3],
            [-1, -1, 1, 0, 0, 3],
            [-1, -1, -1, 4, 5, 5],
            [6, 7, 7, 4, -1, -1],
            [6, -1, -1, 4, 8, 8],
        ]
    )

    assert board.width == 6
    assert board.vehicles == (
        Vehicle(id=0, tiles=((2, 3), (2, 4)), horizontal=True),
        Vehicle(id=1, tiles=((0, 2), (1, 2), (2, 2)), horizontal=False),
        Vehicle(id=2, tiles=((0, 3), (0, 4)), horizontal=True),
        Vehicle(id=3, tiles=((0, 5), (1, 5), (2, 5)), horizontal=False),
        Vehicle(id=4, tiles=((3, 3), (4, 3), (5, 3)), horizontal=False),
        Vehicle(id=5, tiles=((3, 4), (3, 5)), horizontal=True),
        Vehicle(id=6, tiles=((4, 0), (5, 0)), horizontal=False),
        Vehicle(id=7, tiles=((4, 1), (4, 2)), horizontal=True),
        Vehicle(id=8, tiles=((5, 4), (5, 5)), horizontal=True),
    )


@pytest.mark.parametrize(
    "matrix, expected_result",
    [
        (
            [
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, 0, 0, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
            ],
            False,
        ),
        (
            [
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, 0, 0],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
            ],
            True,
        ),
        (
            [
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, 0, 0],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
            ],
            True,
        ),
    ],
)
def test_is_final_configuration(matrix: list[list[int]], expected_result: bool):
    assert Board.from_matrix(matrix=matrix).is_final_configuration() == expected_result


@pytest.mark.parametrize(
    "matrix, expected_result",
    [
        (
            [
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, 0, 0, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
            ],
            1,
        ),
        (
            [
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, 0, 0],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
            ],
            0,
        ),
        (
            [
                [-1, -1, -1, -1, -1, -1],
                [0, 0, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1],
            ],
            4,
        ),
    ],
)
def test_calculate_number_of_tiles_from_exit(matrix: list[list[int]], expected_result: int):
    assert len(Board.from_matrix(matrix=matrix).get_tiles_to_cover_by_red()) == expected_result

    
    
