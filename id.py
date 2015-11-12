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

def iterative_deepening():
    stack = collections.deque()
    stack.appendleft(root)
    states = set()
    max = 0
    while len(stack) > 0:
        node = stack.popleft()
        if node.depth < max:
            for car in cars:
                for move in car.get_moves(node):
                    child = rhutils.Board(node, (car.id, move), node.depth + 1)
                    car.move(move, child)
                    if child.get_hash_value() not in states:
                        states.add(child.get_hash_value())
                        if child.board[row][col] == 99:
                            return child
                        stack.appendleft(child)

        if len(stack) == 0:
            states = set()
            states.add(root.get_hash_value())
            stack.appendleft(root)
            max += 1



start = timer()
current = iterative_deepening()
moves = collections.deque()
while current.parent is not None:
    moves.appendleft(current.move)
    current = current.parent
print len(moves)
end = timer()
print end - start