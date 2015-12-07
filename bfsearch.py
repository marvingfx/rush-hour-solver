import sys, rushutils_uninformed, os.path, visualisation
from timeit import default_timer as timer


def bfs():
    while len(queue) > 0:
        node = queue.pop(0)
        for move in node.get_moves():
            child = node.move(move[0], move[1])
            if move[0] == 0:
                if child.win():
                    return child
            if child.get_hash() not in states:
                states.add(child.get_hash())
                queue.append(child)

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

    # initialize queue and states archive
    states = set()
    queue = list()
    states.add(root.get_hash())
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
print "\nExplored %d states in %f seconds" % (len(states), (end - start))
print "\nSolved in %d moves" % (len(moves))
print moves
print

# start visualisation if wanted
if raw_input("visualisation? (Y/N): ").lower() == 'y':
    vis = visualisation.Visualisation(root, moves)
