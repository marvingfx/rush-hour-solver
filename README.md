# RUSH HOUR SOLVER
This project focuses on writing algorithms that solve the [Rush Hour](http://thinkfun.com/play-online/rush-hour/) game. Both uninformed and informed search algorithms have been implemented. This project includes a number of boards. Board sizes vary from 6x6 to 12x12. Custom boards can easily be created and solved without altering the scripts.

## Installation
1. Make sure you have python installed (check [pyproject.toml](pyproject.toml) for which python version), preferable via [pyenv](https://github.com/pyenv/pyenv) or [pyenv-win](https://github.com/pyenv-win/pyenv-win) or similar python version managers.
2. Install [poetry](https://python-poetry.org).
3. Clone the repository.
4. Execute `poetry install` in the root of the repository.

## Running the code
Once everything is installed, you can run `python solver.py --algorithm [ALROGRITHM] --board [BOARD CSV]`. Use `python solver.py --help
` to find what the options are.

## Creating custom boards
Custom boards have to fulfill a couple of requirements:
* The red car has to be represented by `0`
* Empty tiles need to be represented by `-1` (or any negative number)
* All other vehicles need to be represented by integers bigger than `0`

## TODO
- [ ] Modify cost functions to include more information.
- [ ] Implement more algorithms
- [ ] Implement tests
- [ ] Fix typing / formatting / syntax issues
- [ ] OUTPUT: return path
- [ ] OUTPUT: visualize path
   