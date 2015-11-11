import sys
import os.path
import boardUtils
import collections
from timeit import default_timer as timer


def depth_first_search(node):
    states.add(node.get_hash_value())
    for car in cars:
        for move in car.get_moves(node):
            new_node = car.move(move, node)
            if new_node.get_hash_value() not in states:
                depth_first_search(new_node)



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

# load board from file
else:
    parent = boardUtils.Board()
    parent.load(sys.argv[1])

    # load cars
    cars = boardUtils.get_vehicles(parent)

    # set the row and column for which has to be ch
    if len(parent.board) % 2 == 0:
        row = (len(parent.board) / 2) - 1
    else:
        row = len(parent.board) / 2
    col = len(parent.board) - 1

    # initialize stack and states
    stack = collections.deque()
    states = set()

    routes = []

    # add parent to stack and states
    stack.append(parent)
    # states.add(parent.get_hash_value())

start = timer()
sys.setrecursionlimit(100000)
depth_first_search(parent)
print str(len(states)) + " states saved"
# routes.sort(key=len)
# for route in routes:
#     print route
end = timer()
print str(end - start) + ' seconds elapsed'


