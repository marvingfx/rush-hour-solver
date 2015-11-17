import sys, rushutils, os.path, collections
from timeit import default_timer as timer


def iterative_deepening(root):
    states = dict()
    stack = collections.deque()
    next = collections.deque()
    max_depth = 0
    stack.append(root)
    states[root.get_hash()] = root.depth

    while len(stack) > 0:
        node = stack.popleft()
        if node.depth < max_depth:
            for move in node.get_moves():
                child = node.move(move[0], move[1])
                if child.win():
                    return child
                if not states.__contains__(child.get_hash):
                    states[child.get_hash()] = child.depth
                    stack.appendleft(child)

        else:
            next.appendleft(node)

        if len(stack) == 0:
            stack.extendleft(next)
            next.clear()
            max_depth += 1





def depth_first_search(node):
    if node.win():
        return node
    for move in node.get_moves():
        child = node.move(move[0], move[1])
        if child.get_hash() not in states:
            states.add(node.get_hash())
            test = depth_first_search(child)
            if test:
                return test


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
    # states = set()
    # states.add(root.get_hash())

    sys.setrecursionlimit(100000)

# start the timer
start = timer()

# get first route to solution
current = iterative_deepening(root)

# stop the timer
end = timer()


# get the moves from to the winning state

moves = collections.deque()
while current.parent is not None:
    moves.appendleft(current.moved)
    current = current.parent

print len(moves)

# print results
print "\nSolved in the time of %f seconds" % (end - start)
print
