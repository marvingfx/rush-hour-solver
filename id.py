import sys, rushutils, os.path, collections, visualisation
from timeit import default_timer as timer


def iterative_deepening(root):
    """
    calculates one optimal path to a winning state
    :return: a winning node if a solution is found, or nothing if board is unsolvable
    """
    max_depth = 0

    while len(stack):

        # get the first node from the stack
        node = stack.popleft()

        # generate all possible children if the depth of the node is below the maximum depth
        if node.depth < max_depth:
            for move in node.get_moves():
                child = node.move(move[0], move[1])

                # check if child has already been processed
                if child.get_hash() not in closed:

                    # add child to closed list and to the stack
                    closed[child.get_hash()] = [node.vehicles, move, child.depth]
                    stack.appendleft(child)

                    # check if current child is a solution
                    if move[0] == 0:
                        if child.win():
                            return child.get_hash()

                # check if the depth of the current node is lower than the initial node
                else:
                    if closed[child.get_hash()][2] > child.depth:

                        # update closed list and add child to the stack
                        closed[child.get_hash()] = [node.vehicles, move, child.depth]
                        stack.appendleft(child)

        # continue search with the nodes saved in the open list and increase the maximum depth
        if len(stack) == 0:
            stack.append(root)
            closed.clear()
            closed[root.get_hash()] = [None, None, 0]
            max_depth += 1


# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python id.py <board.txt>"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python id.py <board.txt>"
    sys.exit()

# load board from file
else:

    # initialize root node
    root = rushutils.Board()
    root.load_from_file(sys.argv[1])

    # initialize queue and closed archive
    closed = dict()
    closed[root.get_hash()] = [None, None, 0]
    stack = collections.deque()
    stack.append(root)


# start the timer
start = timer()

# get first route to solution
node = iterative_deepening(root)

# stop the timer
end = timer()


# get the moves to the winning state
moves = []
while closed[node][0] is not None:
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
