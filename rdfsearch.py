import sys, rushutils, os.path, random
from timeit import default_timer as timer


def rdfs():
    """
    Continually searches for shorter solution. Moves are shuffled to be able to
    generate shorter paths
    """

    # initialize stack and closed archive
    closed = dict()
    closed[root.get_hash()] = None
    stack = list()
    stack.append(root)

    # intialize iteration counter
    i = 1

    # set depth limit
    maximum = 100000

    # start the timer
    start = timer()

    while len(stack):

        # get the top node from the stack
        node = stack.pop()

        if node.depth < maximum - 1:
            # generate all possible children
            moves = node.get_moves()
            random.shuffle(moves)
            for move in moves:
                child = node.move(move[0], move[1])

                # check if child has already been processed
                if child.get_hash() not in closed:

                    # add child to closed list and to the stack
                    closed[child.get_hash()] = [node.vehicles, move]
                    stack.append(child)

                # check if current child is a solution
                if move[0] == 0:
                    if child.win():

                        # print results
                        print "\nExplored %d states in %f seconds" % (len(closed), (timer() - start))
                        print "Current shortest path takes %d moves" % child.depth
                        print "Current iteration %d" % i

                        # start over with new maximum
                        stack = list()
                        stack.append(root)
                        closed.clear()
                        closed[root.get_hash()] = None
                        i += 1
                        maximum = child.depth
                        start = timer()
                        break

        # start over
        else:
            stack = list()
            stack.append(root)
            closed.clear()
            closed[root.get_hash()] = None
            i += 1
            start = timer()

# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python rdfsearch.py <board.txt>"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python rdfsearch.py <board.txt>"
    sys.exit()

# load board from file
else:

    # initialize root node
    root = rushutils.Board()
    root.load_from_file(sys.argv[1])

# get a path
rdfs()
