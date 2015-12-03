import sys, rushutils_uninformed, os.path
from timeit import default_timer as timer


def dfs():
    while len(stack) > 0:
        node = stack.pop()
        for move in node.get_moves():
            child = node.move(move[0], move[1])
            if move[0] == 0:
                if child.win():
                    solutions.append(child)
            if child.get_hash() not in states:
                states.add(child.get_hash())
                stack.append(child)

# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python dfsearch.py <board.txt>"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python dfsearch.py <board.txt>"
    sys.exit()

# load board from file
else:

    # initialize root node
    root = rushutils_uninformed.Board()
    root.load_from_file(sys.argv[1])

    # initialize queue and states archive
    states = set()
    stack = list()
    solutions = list()
    states.add(root.get_hash())
    stack.append(root)

# start the timer
start = timer()

# get first route to solution
dfs()

# stop the timer
end = timer()

# get the moves from to the winning state
shortest_solution = list()
for endpoint in solutions:
    solution = list()
    current = endpoint
    while current.parent is not None:
        solution.append(current.moved)
        current = current.parent
    if len(shortest_solution) == 0 or len(shortest_solution) > len(solution):
        solution.reverse()
        shortest_solution = solution

# print results
print "\nExplored %d states in %f seconds" % (len(states), (end - start))
print "\nFound %d solutions, shortest solution takes %d moves" % (len(solutions), len(shortest_solution))
print shortest_solution
print
