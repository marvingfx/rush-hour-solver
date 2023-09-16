from __future__ import annotations

from dataclasses import dataclass, field

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
