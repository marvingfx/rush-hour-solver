## RUSH HOUR SOLVER
This project focuses on writing algorithms that solve the [Rush Hour](http://thinkfun.com/play-online/rush-hour/) game. Both uninformed and informed search algorithms have been implemented. 

This project includes a number of boards. Board sizes vary from 6x6 to 12x12. Custom boards can easily be created and solved without altering the scripts.

**custom boards conditions**

* The board has to be square
* The red vehicle has to be indicated by '?'
* The red vehicle has to be in center row if the board width is odd, or in the center row - 1 if the board width is even
* Empty tiles have to be indicated by '.'
* Vehicles can only be indicated by 1 character, number, or symbol (with the exception of ',')
* Vehicles can only be 2 or 3 tiles long

*example*

	.,.,.,.,.,.
	.,o,o,o,.,.
	.,?,?,9,/,x
	.,.,.,9,/,x
	.,.,.,.,.,.
	.,.,.,.,.,.



**Installation**

* Install [Python](https://www.python.org/) 2.7.10 or higher or [PyPy](http://pypy.org/)*
* Install [Pygame](http://www.pygame.org/download.shtml) (for visualisations)

*disable visualisations if you run PyPy

## Algorithms

**Note**<br>
Larger boards (9x9, 12x12) may require the algorithms to run for several hours

#### Depth First Search
	python depthFirstSearch boards/board.txt
-
#### Iterative Deepening
	python iterativeDeepening.py boards/board.txt
-
#### Depth Limited Stochastic Depth First Search
	python randomDepthFirstSearch.py boards/board.txt
Continually searches for a better solution, and does not visualise the solution.
To quit the algorithm: <kbd>CTRL</kbd> + <kbd>C</kbd>

-
#### Breadth First Search
	python breadthFirstSearch.py boards/board.txt
-
#### A* Search
	python aStarSearch.py boards/board.txt
-
#### Beam Search
	python beamSearch.py boards/board.txt (width)
width = 3 if no width is supplied



## Visualisation
Solutions can be visualised after the algorithms finish (except for stochastic depth first search). The visualisation can also be started manually. The script will ask you to enter a string of a board, and a tuple of a path.

	python standalone_vis.py

*Lirry Pinter (10565051)<br>
Maartje Kruijt (10430563)<br>
Marvin Straathof (10353860)*
   