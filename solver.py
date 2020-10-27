from model.board import Board
from algorithm.algorithm import breadth_first_search, depth_first_search, a_star

if __name__ == '__main__':
    board = Board.from_matrix([
        [-1, -1, 1, 2, 2, 3],
        [-1, -1, 1, -1, -1, 3],
        [-1, -1, 1, 0, 0, 3],
        [-1, -1, -1, 5, 4, 4],
        [8, 7, 7, 5, -1, -1],
        [8, -1, -1, 5, 6, 6]
    ])

    methods = [breadth_first_search, depth_first_search, a_star]
    for method in methods:
        result = method(board)
        print(
            f'found solution of {result.node.depth} '
            f'steps with {method.__name__}. '
            f'Explored {result.number_of_explored_states} states.'
        )
