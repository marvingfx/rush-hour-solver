import rhutils
import sys
import os.path
import collections
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

# load board from file
else:
    root = rhutils.Board(None, None, 0)
    root.load_from_file(sys.argv[1])
    cars = rhutils.get_vehicles(root)

    # set the row and column for which has to be ch
    if len(root.board) % 2 == 0:
        row = (len(root.board) / 2) - 1
    else:
        row = len(root.board) / 2
    col = len(root.board) - 1

    for car in cars:
        print car
        print car.get_moves(root)

    # initialize queue and states
    queue = list()
    states = set()

    queue.append(root)
    states.add(root)

def BFS():
    while len(queue) > 0:
        node = queue.pop(0)
        for car in cars:
            for move in car.get_moves(node):
                child = rhutils.Board(node, (car.id, move), node.depth + 1)
                car.move(move, child)
                if child.board[row][col] == 99:
                    return child
                if child.get_hash_value() not in states:
                    queue.append(child)
                    states.add(child.get_hash_value())




start = timer()
current = BFS()
end = timer()

print len(states)
moves = collections.deque()
while current.parent is not None:
    moves.appendleft(current.move)
    current = current.parent
print len(moves)
print end - start



