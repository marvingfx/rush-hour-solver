import sys
import os.path
import boardUtils
from timeit import default_timer as timer

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

# load the board
else:
    parent = boardUtils.Board()
    parent.load(sys.argv[1])
    cars = boardUtils.get_vehicles(parent)
    if len(parent.board) % 2 == 0:
        row = (len(parent.board) / 2) - 1
    else:
        row = len(parent.board) / 2
    col = len(parent.board) - 1
    states = set()
    stack = list()
    stack.append(parent)



def DFS(graph,start,goal):
   stack = [(start, [start])]
   while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))



start = timer()
end = timer()
print str(end - start) + ' seconds elapsed'


