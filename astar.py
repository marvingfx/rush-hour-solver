import sys, rushutils, os.path, heapq
from timeit import default_timer as timer

@profile
def astar():
    while len(pqueue):
        node = heapq.heappop(pqueue)
        for move in node.get_moves():
            child = node.move(move[0], move[1])
            if child not in states:
                states[child] = [node.vehicles, move]
                heapq.heappush(pqueue, child)
            if move[0] == 0:
                if child.win():
                    return child

# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python astar.py <board.txt>"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python astar.py <board.txt>"
    sys.exit()

# load board from file
else:

    # initialize root node
    root = rushutils.Board()
    root.load_from_file(sys.argv[1])

    # initialize priority queue and states archive
    states = dict()
    pqueue = list()
    states[root] = None
    heapq.heappush(pqueue, root)

# start the timer
start = timer()

# get first route to solution
hash = astar()

# stop the timer
end = timer()

# get the moves from to the winning state
moves = []
while states[hash] is not None:
    moves.append(states[hash][1])
    hash = tuple(states[hash][0])
moves.reverse()

# print results
print "\nExplored %d states in %f seconds" % (len(states), (end - start))
print "\nSolved in %d moves" % (len(moves))
print moves
print

