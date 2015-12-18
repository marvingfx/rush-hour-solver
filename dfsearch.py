import sys, rushutils, os.path, visualisation
from timeit import default_timer as timer


def dfs():
    """
    calculates a path to a winning state
    """
    while len(stack):

        # get the top node from the stack
        node = stack.pop()

        # generate all possible children
        for move in node.get_moves():
            child = node.move(move[0], move[1])

            # check if child has already been processed
            if child.get_hash() not in closed:

                # add child to closed list and to the stack
                closed[child.get_hash()] = [node.vehicles, move]
                stack.append(child)

            # check if current child is a solution
            if move[0] == 0:

                # add winning configuration to solutions list
                if child.win():
                    solutions.append(child.get_hash())

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
    root = rushutils.Board()
    root.load_from_file(sys.argv[1])

    # initialize stack, solutions list, and closed archive
    closed = dict()
    closed[root.get_hash()] = None
    stack = list()
    stack.append(root)
    solutions = list()

# start the timer
start = timer()

# get first route to solution
dfs()

# stop the timer
end = timer()

# get the shortest path to solution from all possible solutions
shortest_solution = list()
for node in solutions:
    solution = list()
    while closed[node] is not None:
        solution.append(closed[node][1])
        node = closed[node][0]

    # determine if solution is shorter than current shortest solution
    if len(shortest_solution) == 0 or len(shortest_solution) > len(solution):
        solution.reverse()
        shortest_solution = solution

# print results
print "\nExplored %d states in %f seconds" % (len(closed), (end - start))
print "\nFound %d solutions, shortest solution takes %d moves" % (len(solutions), len(shortest_solution))
print shortest_solution
print

# start visualisation if wanted
if raw_input("View visualisation of solution? (Y/N): ").lower() == 'y':
    vis = visualisation.Visualisation(root, shortest_solution)
