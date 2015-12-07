import sys, rushutils, os.path, heapq, visualisation
from timeit import default_timer as timer


def beamsearch(width):
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
        if len(beam) < width:
            for node in beam:
                heapq.heappush(pqueue, node)
        else:
            for index in range(width):
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
    width = 3


    # beam width information
    if len(sys.argv) > 2:
        width = int(sys.argv[2])
        print "Using beam width of %d" % width
    else:
        print "Using default beam width of %d" % width

    # initialize root node
    root = rushutils.Board()
    root.load_from_file(sys.argv[1])

    # initialize priority queue and states archive
    states = set()
    pqueue = list()
    states.add(root.get_hash())
    heapq.heappush(pqueue, root)

# start the timer
start = timer()

# get first route to solution
current = beamsearch(width)

# stop the timer
end = timer()

# get the moves from to the winning state
moves = []
while current.parent is not None:
    moves.append(current.moved)
    current = current.parent
moves.reverse()

# print results
print "\nExplored %d states in %f seconds" % (len(states), (end - start))
print "\nSolved in %d moves" % (len(moves))
print moves
print

# start visualisation if wanted
if raw_input("visualisation? (Y/N): ").lower() == 'y':
    vis = visualisation.Visualisation(root, moves)
