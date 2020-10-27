from dataclasses import dataclass

from model.board import Board


@dataclass(frozen=True)
class Node:
    board: Board = None
    depth: int = 0
    value: int = 0

    def __lt__(self, other):
        return self.value < other.value


@dataclass(frozen=True)
class ChildNode(Node):
    parent: Node = None
