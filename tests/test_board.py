from src.model import Board


def test_from_matrix():
    assert Board.from_matrix(
        [
            [-1, -1, 1, 2, 2, 3],
            [-1, -1, 1, -1, -1, 3],
            [-1, -1, 1, 0, 0, 3],
            [-1, -1, -1, 4, 5, 5],
            [6, 7, 7, 4, -1, -1],
            [6, -1, -1, 4, 8, 8],
        ]
    )
