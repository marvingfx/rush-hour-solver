import sys, rushutils, os.path, visualisation
from timeit import default_timer as timer


def beamsearch(width):
    """
    calculates one  path to a winning state
    :param width: width of the beam
    :return: a winning node if a solution is found, or nothing if board is unsolvable
    """
    while len(queue):

        # get the first node from the queue
        node = queue.pop(0)

        # initialize beam
        beam = list()

        # generate all possible children
        for move in node.get_moves():
            child = node.move(move[0], move[1])

            # check if current child is a solution
            if move[0] == 0:
                if child.win():
                    closed[child.get_hash()] = [node.vehicles, child.moved]
                    return child.get_hash()

            # add child to beam if not processed already
            if child.get_hash() not in closed:
                beam.append(child)

        # sort the beam so that the most promising members are in front
        beam.sort()

        # add n children to the queue
        for i, child in enumerate(beam):
            if i < width:
                closed[child.get_hash()] = [node.vehicles, child.moved]
                queue.append(child)

# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python beamSearch.py <board.txt> (width)"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python beamSearch.py <board.txt> (width)"
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

    # initialize queue and closed archive
    closed = dict()
    closed[root.get_hash()] = None
    queue = list()
    queue.append(root)

# start the timer
start = timer()

# get first route to solution
node = beamsearch(width)

# stop the timer
end = timer()

# get the moves from to the winning state
moves = []
while closed[node] is not None:
    moves.append(closed[node][1])
    node = closed[node][0]
moves.reverse()

# print results
print "\nExplored %d states in %f seconds" % (len(closed), (end - start))
print "\nSolved in %d moves" % (len(moves))
print moves
print

# start visualisation if wanted
if raw_input("View visualisation of solution? (Y/N): ").lower() == 'y':
    vis = visualisation.Visualisation(root, moves)
