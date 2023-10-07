import time
from typing import Callable

import click

from .algorithm import (
    Result,
    a_star,
    beam_search,
    breadth_first_search,
    depth_first_search,
)
from .model import Board, get_history

ALGORITHM_NAME_MAPPING: dict[str, Callable[[Board], Result]] = {
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
    help="The algorighm of your choosing to solve the board",
)
@click.option(
    "--board",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="The path of the board file that you want to solve",
)
@click.option(
    "--visualize",
    is_flag=True,
    help="""Whether you want to interactively visualize the solution.
    Note that colours might not work well with Windows:
    (https://click.palletsprojects.com/en/8.1.x/utils/#ansi-colors)
    """,
)
def solve(
    algorithm: str,
    board: str,
    visualize: bool,
) -> None:
    algorithm_implementation = ALGORITHM_NAME_MAPPING[algorithm]
    board_to_solve = Board.from_csv(board)

    start = time.perf_counter()
    result = algorithm_implementation(board_to_solve)
    end = time.perf_counter()

    if visualize:
        boards = get_history(result.node)

        for board_from_node in boards:
            click.clear()
            click.echo(board_to_colourized_click_output(board_from_node))
            click.pause()

    click.echo(
        f"Found solution at depth {result.node.depth} with {algorithm_implementation.__name__}"  # noqa: E501
    )
    click.echo(
        f"Explored {result.number_of_explored_states} states states in {end - start} seconds."  # noqa: E501
    )


def board_to_colourized_click_output(board: Board) -> str:
    background_colour = "black"
    character_to_use = "██"
    default_colours = [
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        "bright_black",
        "bright_red",
        "bright_green",
        "bright_yellow",
        "bright_blue",
        "bright_magenta",
        "bright_cyan",
        "bright_white",
    ]

    tile_id_to_colour = {
        vehicle.id: "red"
        if vehicle.id == 0
        else default_colours[
            index - 1 if index < len(default_colours) else index % len(default_colours)
        ]
        for index, vehicle in enumerate(board.vehicles)
    } | {-1: "black"}

    return_string = ""

    for row in board.to_matrix():
        for column in row:
            return_string += click.style(
                character_to_use, bg=background_colour, fg=tile_id_to_colour[column]
            )
        return_string += "\n"

    return return_string


if __name__ == "__main__":
    solve()
