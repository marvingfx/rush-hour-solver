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
    cars = boardUtils.get_vehicles(parent)
    if len(parent.board) % 2 == 0:
        row = (len(parent.board) / 2) - 1
    else:
        row = len(parent.board) / 2
    col = len(parent.board) - 1
    states = set()
    stack = list()
    stack.append(parent)



def DFS():
   while stack:
       node = stack.pop()
       for car in cars:
            moves = car.get_moves(node)
            if moves:
                for move in moves:
                    child = car.move(move, node)
                    if (child not in states):
                        states.add(child)
                    else:
                        if(child.board[row][col] == 99):
                            print child
                        else:
                            stack.push(child)






start = timer()
print DFS()
end = timer()
print str(end - start) + ' seconds elapsed'


