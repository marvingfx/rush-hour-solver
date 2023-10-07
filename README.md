# RUSH HOUR SOLVER
This project focuses on writing algorithms that solve the [Rush Hour](http://thinkfun.com/play-online/rush-hour/) game. Both uninformed and informed search algorithms have been implemented. This project includes a number of boards. Board sizes vary from 6x6 to 12x12. Custom boards can easily be created and solved without altering the scripts.

## Installation
1. Make sure you have python installed (check [pyproject.toml](pyproject.toml) for which python version), preferable via [pyenv](https://github.com/pyenv/pyenv) or [pyenv-win](https://github.com/pyenv-win/pyenv-win) or similar python version managers.
2. Install [poetry](https://python-poetry.org).
3. Clone the repository.
4. Execute `poetry install` in the root of the repository.

## Usage
```
Usage: python -m src.solver [OPTIONS]

Options:
  --algorithm [astar|beam|bfs|dfs]
                                  The algorighm of your choosing to solve the
                                  board  [required]
  --board PATH                    The path of the board file that you want to
                                  solve  [required]
  --visualize                     Whether you want to interactively visualize
                                  the solution
  --help                          Show this message and exit.
```
For example: `python -m src.solver --board boards/board1.csv --algorithm bfs --visualize`

## Creating custom boards
Custom boards have to fulfill a couple of requirements:
* The red car has to be represented by `0`
* Empty tiles need to be represented by `-1` (or any negative number)
* All other vehicles need to be represented by integers bigger than `0`

## TODO
- [ ] Modify cost functions to include more information.
- [ ] Implement more algorithms
- [ ] Implement tests
- [ ] OUTPUT: return path
   