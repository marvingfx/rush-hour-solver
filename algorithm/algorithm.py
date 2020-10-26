from model.node import Node, ChildNode
from model.board import Board


def breadth_first_search(board: Board, max_depth: int = 1000) -> Node:
    depth = 0
    visited_nodes = set()
    queue = list([Node(board, depth)])

    while len(queue) & depth < max_depth:
        current_node = queue.pop(0)
        depth = current_node.depth

        if current_node.board.is_final_configuration():
            return current_node
        else:
            for possible_move in current_node.board.get_moves():
                child_board = current_node.board.move_vehicle(move=possible_move)

                if child_board not in visited_nodes:
                    visited_nodes.add(child_board)
                    queue.append(ChildNode(board=child_board, parent=current_node, depth=depth + 1))


def depth_first_search(board: Board, max_depth: int = 10000) -> Node:
    depth = 0
    visited_nodes = set()
    queue = list([Node(board, depth)])

    while len(queue) & depth < max_depth:
        current_node = queue.pop()
        depth = current_node.depth

        if current_node.board.is_final_configuration():
            return current_node
        else:
            for possible_move in current_node.board.get_moves():
                child_board = current_node.board.move_vehicle(move=possible_move)

                if child_board not in visited_nodes:
                    visited_nodes.add(child_board)
                    queue.append(ChildNode(board=child_board, parent=current_node, depth=depth + 1))
