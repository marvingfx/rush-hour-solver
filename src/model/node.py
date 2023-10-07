from __future__ import annotations

from dataclasses import dataclass, field
from functools import reduce

from ..model.board import Board


@dataclass(frozen=True)
class Node:
    parent: Node | None = None
    board: Board = field(default=Board())
    depth: int = 0
    value: int = 0

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value


def get_history(node) -> list[Board]:
    board_history: list[Board] = []
    current_node = node

    while current_node:
        board = current_node.board
        board_history.insert(0, board)
        current_node = current_node.parent

    return board_history
