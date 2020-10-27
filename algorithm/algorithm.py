from model.node import Node, ChildNode
from model.board import Board
import heapq
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    node: Node
    number_of_explored_states: int


def breadth_first_search(board: Board, max_depth: int = 1000) -> Result:
    depth = 0
    visited_nodes = set()
    queue = list([Node(board, depth)])

    while len(queue) & depth < max_depth:
        current_node = queue.pop(0)
        depth = current_node.depth

        if current_node.board.is_final_configuration():
            return Result(current_node, len(visited_nodes))
        else:
            for possible_move in current_node.board.get_moves():
                child_board = current_node.board.move_vehicle(move=possible_move)

                if child_board not in visited_nodes:
                    visited_nodes.add(child_board)
                    queue.append(ChildNode(board=child_board, parent=current_node, depth=depth + 1))


def depth_first_search(board: Board, max_depth: int = 10000) -> Result:
    depth = 0
    visited_nodes = set()
    queue = list([Node(board, depth)])

    while len(queue) & depth < max_depth:
        current_node = queue.pop()
        depth = current_node.depth

        if current_node.board.is_final_configuration():
            return Result(current_node, len(visited_nodes))
        else:
            for possible_move in current_node.board.get_moves():
                child_board = current_node.board.move_vehicle(move=possible_move)

                if child_board not in visited_nodes:
                    visited_nodes.add(child_board)
                    queue.append(ChildNode(board=child_board, parent=current_node, depth=depth + 1))


def a_star(board: Board, max_depth: int = 1000) -> Result:
    depth = 0
    visited_nodes = set()
    sorted_list = list()
    root = Node(board, depth)
    heapq.heappush(sorted_list, root)

    while len(sorted_list) & depth < max_depth:
        current_node = heapq.heappop(sorted_list)
        depth = current_node.depth

        if current_node.board.is_final_configuration():
            return Result(current_node, len(visited_nodes))
        else:
            for possible_move in current_node.board.get_moves():
                child_board = current_node.board.move_vehicle(move=possible_move)

                if child_board not in visited_nodes:
                    visited_nodes.add(child_board)
                    heapq.heappush(sorted_list, ChildNode(board=child_board, parent=current_node, depth=depth + 1,
                                                          value=child_board.score() + depth))
