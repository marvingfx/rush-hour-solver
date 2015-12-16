import sys, rushutils, os.path, heapq, visualisation
from timeit import default_timer as timer


def astar():
    """
    calculates one optimal path to a winning state by applying an admissable heuristic
    :return: a winning node if a solution is found, or nothing if board is unsolvable
    """
    while len(pqueue):

        # get the node with the lowest cost estimate
        node = heapq.heappop(pqueue)

        # generate all possible children
        for move in node.get_moves():
            child = node.move(move[0], move[1])

            # check if child has already been processed
            if child.get_hash() not in closed:

                # add child to closed list and to the priority queue
                closed[child.get_hash()] = [node.vehicles, move]
                heapq.heappush(pqueue, child)

            # check if current child is a solution
            if move[0] == 0:
                if child.win():
                    return child.get_hash()

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

    # initialize priority queue and closed archive
    closed = dict()
    closed[root.get_hash()] = None
    pqueue = list()
    heapq.heappush(pqueue, root)

# start the timer
start = timer()

# get first route to solution
node = astar()

# stop the timer
end = timer()

# get the moves to the winning node
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
