import sys, rushutils, os.path, heapq
from timeit import default_timer as timer

WIDTH = 3


def astar():
    while len(pqueue) > 0:
        node = heapq.heappop(pqueue)
        beam = list()
        for move in node.get_moves():
            child = node.move(move[0], move[1])
            if move[0] == 0:
                if child.win():
                    return child
            if child.get_hash() not in states:
                states.add(child.get_hash())
                beam.append(child)
            else:
                del child
        beam.sort()
        if len(beam) < WIDTH:
            for node in beam:
                heapq.heappush(pqueue, node)
        else:
            for index in range(WIDTH):
                heapq.heappush(pqueue, beam[index])

# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python beam.py <board.txt> width"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python beam.py <board.txt> width"
    sys.exit()

# load board from file
else:

    # beam width information
    if len(sys.argv) > 2:
        WIDTH = int(sys.argv[2])
        print "Using beam width of %d" % WIDTH
    else:
        print "Using default beam width of %d" % WIDTH

    # initialize root node
    root = rushutils.Board()
    root.load_from_file(sys.argv[1])

    # initialize priority queue and states archive
    states = set()
    pqueue = list()
    states.add(root.get_hash())
    heapq.heappush(pqueue, root)

start = timer()
current = astar()
end = timer()

moves = []
while current.parent is not None:
    moves.append(current.moved)
    current = current.parent
moves.reverse()

print "\nExplored %d states in %f seconds" % (len(states), (end - start))
print "\nSolved in %d moves" % (len(moves))
print moves
print
