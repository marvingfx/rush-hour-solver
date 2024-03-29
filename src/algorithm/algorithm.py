import collections
import heapq
from collections import deque
from dataclasses import dataclass
from typing import List, MutableSequence, Set

from ..model import Board, Node


class NoSolutionFoundException(Exception):
    pass


@dataclass(frozen=True)
class Result:
    node: Node
    number_of_explored_states: int


def breadth_first_search(board: Board, max_depth: int = 1000) -> Result:
    """Breadth first search
    Does not care about value

    Args:
        board (Board): _description_
        max_depth (int, optional): _description_. Defaults to 1000.

    Raises:
        NoSolutionFoundException: _description_

    Returns:
        Result: _description_
    """
    depth = 0
    visited_boards: Set[Board] = set()
    root = Node(board=board)
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
                    node = Node(board=child_board, parent=current_node, depth=depth + 1)
                    visited_boards.add(child_board)
                    queue.append(node)

                    if child_board.is_final_configuration():
                        return Result(node, len(visited_boards))

    raise NoSolutionFoundException()


def depth_first_search(board: Board, max_depth: int = 10000) -> Result:
    """Depth first search
    Does not care about value

    Args:
        board (Board): _description_
        max_depth (int, optional): _description_. Defaults to 10000.

    Raises:
        NoSolutionFoundException: _description_

    Returns:
        Result: _description_
    """
    depth = 0
    visited_boards: Set[Board] = set()
    root = Node(board=board)
    queue = list([root])

    if root.board.is_final_configuration():
        return Result(root, len(visited_boards))

    while len(queue) & depth < max_depth:
        current_node = queue.pop()
        depth = current_node.depth

        for possible_move in current_node.board.get_moves():
            child_board = current_node.board.move_vehicle(move=possible_move)

            if child_board not in visited_boards:
                node = Node(board=child_board, parent=current_node, depth=depth + 1)
                visited_boards.add(child_board)
                queue.append(node)

                if child_board.is_final_configuration():
                    return Result(node, len(visited_boards))

    raise NoSolutionFoundException


def iterative_deepening_depth_first_search(
    board: Board, max_depth: int = 1000
) -> Result:
    """Iterative deepening dept first search

    Args:
        board (Board): _description_
        max_depth (int, optional): _description_. Defaults to 1000.

    Raises:
        NoSolutionFoundException: _description_

    Returns:
        Result: _description_
    """
    local_max_depth = 1
    visited_boards: Set[Board] = set()
    root = Node(board=board)
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
                node = Node(board=child_board, parent=current_node, depth=depth + 1)
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
    """A start

    Args:
        board (Board): _description_
        max_depth (int, optional): _description_. Defaults to 1000.

    Raises:
        NoSolutionFoundException: _description_

    Returns:
        Result: _description_
    """
    depth = 0
    visited_boards: Set[Board] = set()
    sorted_list: List[Node] = list()
    root = Node(board=board, depth=depth)
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
                node = Node(
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
    """beam search

    Args:
        board (Board): _description_
        width (int, optional): _description_. Defaults to 2.
        max_depth (int, optional): _description_. Defaults to 1000.

    Raises:
        NoSolutionFoundException: _description_

    Returns:
        Result: _description_
    """
    depth = 0
    visited_boards: Set[Board] = set()
    root = Node(board=board, depth=depth)
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
                node = Node(
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
