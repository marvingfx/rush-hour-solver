import sys
import os.path
import boardUtils

# check if file is supplied
if len(sys.argv) <= 1:
    print "No file is supplied"
    print "Usage: python DFS.py <board.txt>"
    sys.exit()

# check if file exists
elif not os.path.isfile(sys.argv[1]):
    print "File can't be loaded"
    print "Usage: python DFS.py <board.txt>"
    sys.exit()

# load the board
else:
    board = ([list(line.strip('\n')) for line in open(sys.argv[1])])
    cars = boardUtils.getCars(board)

# TODO
# recursive function
# stack
# check for move validity
# move
# archive boards and steps