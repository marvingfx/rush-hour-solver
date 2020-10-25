from dataclasses import dataclass

from model.board import Board


@dataclass(frozen=True)
class Node:
    board: Board


@dataclass(frozen=True)
class ChildNode(Node):
    parent: Node
