import sys
import os.path
import boardUtils
from timeit import default_timer as timer

# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python BFS.py <board.txt>"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python BFS.py <board.txt>"
    sys.exit()

# load the board
else:
    parent = boardUtils.Board()
    parent.load(sys.argv[1])
    cars = boardUtils.getcars(parent)
    states = set()
    for car in cars:
        print car
    queue = []
    queue.append(parent)
    queue.append(parent)


def BFS():
    while len(queue) > 0:
        node = queue.pop(0)
        for car in cars:
            moves = car.getmoves(node)
            for move in moves:
                child = car.move(move, node)
                if child.board[2][5] == 99:
                    for row in child.board:
                        print row
                    return
                if child not in states:
                    states.add(child)
                    queue.append(child)

BFS()






start = timer()
end = timer()
print end - start

# TODO
# recursive function
# stack
# check for move validity
# move
# archive boards and steps
# class board + hashing