import sys, rushutils, os.path
from timeit import default_timer as timer


def beamsearch(width):
    while len(queue) > 0:
        node = queue.pop(0)
        beam = list()
        for move in node.get_moves():
            child = node.move(move[0], move[1])
            if move[0] == 0:
                if child.win():
                    states[child.get_hash()] = [node.vehicles, child.moved]
                    return child.get_hash()
            if child.get_hash() not in states:
                beam.append(child)
        beam.sort()
        for i, child in enumerate(beam):
            if i < width:
                states[child.get_hash()] = [node.vehicles, child.moved]
                queue.append(child)

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
    width = 3

    if len(sys.argv) > 2:
        width = int(sys.argv[2])
        print "Using beam width of %d" % width
    else:
        print "Using default beam width of %d" % width

    # initialize root node
    root = rushutils.Board()
    root.load_from_file(sys.argv[1])

    # initialize priority queue and states archive
    states = dict()
    queue = list()
    states[root.get_hash()] = None
    queue.append(root)

# start the timer
start = timer()

# get first route to solution
hash = beamsearch(width)

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

# # start visualisation if wanted
# if raw_input("visualisation? (Y/N): ").lower() == 'y':
#     vis = visualisation.Visualisation(root, moves)
