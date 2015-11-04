import sys
import os.path

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
    board = ([line.strip('\n') for line in open(sys.argv[1])])
    for line in board:
        print line

# exit tile
# board[(len(board) / 2) - 1][len(board) - 1];

# TODO
# recursive function
# stack
# check for move validity
# move
# archive