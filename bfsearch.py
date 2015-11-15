import sys, rushutils, os.path, collections
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
    root = rushutils.Board(None, None, None, None)
    root.load_from_file(sys.argv[1])
    states = set()
    queue = list()
    states.add(root.get_hash())
    queue.append(root)


def bfs():
    while len(queue) > 0:
        node = queue.pop(0)
        for move in node.get_moves():
            child = node.move(move[0], move[1])
            if child.win():
                return child
            if child.get_hash() not in states:
                states.add(child.get_hash())
                queue.append(child)


start = timer()
current = bfs()
print len(states)
end = timer()
moves = collections.deque()
while current.parent is not None:
    moves.appendleft(current.moved)
    current = current.parent
print moves
print end - start
