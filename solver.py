from model.board import Board
from algorithm.algorithm import breadth_first_search, depth_first_search

if __name__ == '__main__':
    board = Board.from_matrix([
        [-1, -1, 1, 2, 2, 3],
        [-1, -1, 1, -1, -1, 3],
        [-1, -1, 1, 0, 0, 3],
        [-1, -1, -1, 5, 4, 4],
        [8, 7, 7, 5, -1, -1],
        [8, -1, -1, 5, 6, 6]
    ])
    node = breadth_first_search(board)
    node = depth_first_search(board)

