import sys, rushutils, os.path, collections, visualisation
from timeit import default_timer as timer


def iterative_deepening():
    max_depth = 0
    open = list()

    while len(stack) > 0:
        node = stack.popleft()
        if node.depth < max_depth:
            for move in node.get_moves():
                child = node.move(move[0], move[1])
                if child.win():
                    return child
                if not states.__contains__(child.get_hash()):
                    states[child.get_hash()] = child.depth
                    stack.appendleft(child)
                else:
                    if states[child.get_hash()] > child.depth:
                        states[child.get_hash()] = child.depth
                        stack.appendleft(child)
        else:
            open.append(node)

        if len(stack) == 0:
            stack.extendleft(open)
            open = list()
            max_depth += 1


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

    # initialize root node
    root = rushutils.Board(None, None, None, None)
    root.load_from_file(sys.argv[1])

    # initialize queue and states archive
    states = dict()
    states[root.get_hash()] = 0
    stack = collections.deque()
    stack.append(root)


# start the timer
start = timer()

# get first route to solution
current = iterative_deepening()

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
