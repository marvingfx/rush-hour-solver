import collections
import heapq
from collections import deque
from dataclasses import dataclass
from typing import List, MutableSequence, Set

from ..model import Board, ChildNode, Node


class NoSolutionFoundException(Exception):
    pass


@dataclass(frozen=True)
class Result:
    node: Node
    number_of_explored_states: int


def breadth_first_search(board: Board, max_depth: int = 1000) -> Result:
    depth = 0
    visited_boards: Set[Board] = set()
    root = Node(board)
    queue = list([root])

    if root.board.is_final_configuration():
        return Result(root, len(visited_boards))

    while len(queue) & depth < max_depth:
        current_node = queue.pop(0)
        depth = current_node.depth

        if current_node.board.is_final_configuration():
            return Result(current_node, len(visited_boards))
        else:
            for possible_move in current_node.board.get_moves():
                child_board = current_node.board.move_vehicle(move=possible_move)

                if child_board not in visited_boards:
                    node = ChildNode(
                        board=child_board, parent=current_node, depth=depth + 1
                    )
                    visited_boards.add(child_board)
                    queue.append(node)

                    if child_board.is_final_configuration():
                        return Result(node, len(visited_boards))

    raise NoSolutionFoundException()


def depth_first_search(board: Board, max_depth: int = 10000) -> Result:
    depth = 0
    visited_boards: Set[Board] = set()
    root = Node(board)
    queue = list([root])

    if root.board.is_final_configuration():
        return Result(root, len(visited_boards))

    while len(queue) & depth < max_depth:
        current_node = queue.pop()
        depth = current_node.depth

        for possible_move in current_node.board.get_moves():
            child_board = current_node.board.move_vehicle(move=possible_move)

            if child_board not in visited_boards:
                node = ChildNode(
                    board=child_board, parent=current_node, depth=depth + 1
                )
                visited_boards.add(child_board)
                queue.append(node)

                if child_board.is_final_configuration():
                    return Result(node, len(visited_boards))

    raise NoSolutionFoundException


def iterative_deepening_depth_first_search(
    board: Board, max_depth: int = 1000
) -> Result:
    local_max_depth = 1
    visited_boards: Set[Board] = set()
    root = Node(board)
    stack: deque[Node] = deque()
    stack.append(root)

    if root.board.is_final_configuration():
        return Result(root, len(visited_boards))

    while len(stack):
        current_node = stack.popleft()
        depth = current_node.depth

        for possible_move in current_node.board.get_moves():
            child_board = current_node.board.move_vehicle(move=possible_move)

            if child_board not in visited_boards and depth <= local_max_depth:
                node = ChildNode(
                    board=child_board, parent=current_node, depth=depth + 1
                )
                visited_boards.add(child_board)
                stack.append(node)

                if child_board.is_final_configuration():
                    return Result(node, len(visited_boards))

        if len(stack) == 0 and local_max_depth <= max_depth:
            stack.append(root)
            visited_boards.clear()
            visited_boards.add(root.board)
            local_max_depth += 1

    raise NoSolutionFoundException


def a_star(board: Board, max_depth: int = 1000) -> Result:
    depth = 0
    visited_boards: Set[Board] = set()
    sorted_list: List[Node] = list()
    root = Node(board, depth)
    heapq.heappush(sorted_list, root)

    if root.board.is_final_configuration():
        return Result(root, len(visited_boards))

    while len(sorted_list) & depth < max_depth:
        current_node = heapq.heappop(sorted_list)
        depth = current_node.depth

        for possible_move in current_node.board.get_moves():
            child_board = current_node.board.move_vehicle(move=possible_move)

            if child_board not in visited_boards:
                visited_boards.add(child_board)
                node = ChildNode(
                    board=child_board,
                    parent=current_node,
                    depth=depth + 1,
                    value=child_board.get_minimum_cost() + depth,
                )
                heapq.heappush(sorted_list, node)

                if child_board.is_final_configuration():
                    return Result(node, len(visited_boards))

    raise NoSolutionFoundException


def beam_search(board: Board, width: int = 2, max_depth: int = 1000) -> Result:
    depth = 0
    visited_boards: Set[Board] = set()
    root = Node(board, depth)
    queue: List[Node] = list([root])

    if root.board.is_final_configuration():
        return Result(root, len(visited_boards))

    while len(queue) & depth < max_depth:
        current_node = queue.pop(0)
        depth = current_node.depth

        beam: List[Node] = list()

        for possible_move in current_node.board.get_moves():
            child_board = current_node.board.move_vehicle(move=possible_move)

            if child_board not in visited_boards:
                visited_boards.add(child_board)
                node = ChildNode(
                    board=child_board,
                    parent=current_node,
                    depth=depth + 1,
                    value=child_board.get_minimum_cost() + depth,
                )

                heapq.heappush(beam, node)

                if child_board.is_final_configuration():
                    return Result(node, len(visited_boards))

        for i, child in enumerate(beam):
            if i < width:
                queue.append(child)

    raise NoSolutionFoundException
