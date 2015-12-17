import sys, rushutils, os.path, visualisation, random
from timeit import default_timer as timer


def dfs():
    """
    calculates a path to a winning state
    """
    maximum = 7538
    begin = timer()
    while len(stack):

        # get the first node from the stack
        node = stack.pop()

        # generate all possible children
        moves = node.get_moves()
        random.shuffle(moves)
        for move in moves:
            child = node.move(move[0], move[1])
            if child.depth >= maximum:
                begin = timer()
                stack.append(root)
                closed.clear()
                closed[root.get_hash()] = None
                maximum = node.depth
                break

            # check if child has already been processed
            if child.get_hash() not in closed:

                # add child to closed list and to the stack
                closed[child.get_hash()] = [node.vehicles, move]
                stack.append(child)

            # check if current child is a solution
            if move[0] == 0:
                if child.win():
                    if child.depth < maximum:
                        print child.depth
                        print timer() - begin, "seconds"
                        begin = timer()
                        maximum = child.depth
                        stack.append(root)
                        closed.clear()
                        closed[root.get_hash()] = None
                    solutions.append(child.get_hash())

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

    # initialize queue, solutions list, and closed archive
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

# get the moves to the winning state
shortest_solution = list()
for path in solutions:
    solution = list()
    node = path
    while closed[node] is not None:
        solution.append(closed[node][1])
        node = closed[node][0]
    if len(shortest_solution) == 0 or len(shortest_solution) > len(solution):
        solution.reverse()
        shortest_solution = solution

# print results
print "\nExplored %d states in %f seconds" % (len(closed), (end - start))
print "\nFound %d solutions, shortest solution takes %d moves" % (len(solutions), len(shortest_solution))
# print shortest_solution
print

# start visualisation if wanted
# if raw_input("View visualisation of solution? (Y/N): ").lower() == 'y':
#     vis = visualisation.Visualisation(root, shortest_solution)
