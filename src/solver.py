import time
from typing import Callable

import click

from .algorithm import (
    a_star,
    beam_search,
    breadth_first_search,
    depth_first_search,
)
from .model import Board

ALGORITHM_NAME_MAPPING: dict[str, Callable] = {
    "astar": a_star,
    "beam": beam_search,
    "bfs": breadth_first_search,
    "dfs": depth_first_search,
}


@click.command()
@click.option(
    "--algorithm",
    required=True,
    type=click.Choice(list(ALGORITHM_NAME_MAPPING.keys()), case_sensitive=True),
)
@click.option(
    "--board",
    required=True,
    type=click.Path(exists=True, readable=True),
)
def solve(algorithm: str, board: str) -> None:
    algorithm_implementation = ALGORITHM_NAME_MAPPING[algorithm]
    board_to_solve = Board.from_csv(board)

    start = time.perf_counter()
    result = algorithm_implementation(board_to_solve)
    end = time.perf_counter()
    print(
        f"Found solution of {result.node.depth} "
        f"steps with {algorithm_implementation.__name__}. "
        f"Explored {result.number_of_explored_states} "
        f"states in {end - start} seconds."
    )


if __name__ == "__main__":
    solve()
