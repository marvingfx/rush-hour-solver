import sys, rushutils_uninformed, os.path, visualisation
from timeit import default_timer as timer


def bfs():
    """
    calculates one optimal path to a winning state
    :return: a winning node if a solution is found, or nothing if board is unsolvable
    """
    while len(queue):

        # get the first node from the queue
        node = queue.pop(0)

        # generate all possible children
        for move in node.get_moves():
            child = node.move(move[0], move[1])

            # check if child has already been processed
            if child not in closed:

                # add child to closed list and to the queue
                closed.add(child)
                queue.append(child)

            # check if current child is a solution
            if move[0] == 0:
                if child.win():
                    return child

# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python bfsearch.py <board.txt>"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python bfsearch.py <board.txt>"
    sys.exit()

# load board from file
else:

    # initialize root node
    root = rushutils_uninformed.Board()
    root.load_from_file(sys.argv[1])

    # initialize queue and closed archive
    closed = set()
    closed.add(root)
    queue = list()
    queue.append(root)

# start the timer
start = timer()

# get first route to solution
current = bfs()

# stop the timer
end = timer()

# get the moves from to the winning state
moves = []
while current.parent is not None:
    moves.append(current.moved)
    current = current.parent
moves.reverse()

# print results
print "\nExplored %d states in %f seconds" % (len(closed), (end - start))
print "\nSolved in %d moves" % (len(moves))
print moves
print

# start visualisation if wanted
if raw_input("View visualisation of solution? (Y/N): ").lower() == 'y':
    vis = visualisation.Visualisation(root, moves)
