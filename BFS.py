import sys
import os.path
import boardUtils
from timeit import default_timer as timer


def breadth_first_search():
    """
    Performs a breadth first search for a shortest solution for rush hour
    :return: path to winning board
    """
    while len(queue) > 0:

        # get the first state from queue
        node = queue.pop(0)

        # generate new nodes if the cars can move
        for car in cars:
            for move in car.get_moves(node):

                # create new node
                new_node = car.move(move, node)

                # check if the current node is a winning board setup
                if new_node.board[row][col] == 99:
                    print 'Saved ' + str(len(states)) + ' states'
                    print str(len(new_node.path)) + ' steps taken'
                    return new_node.path

                # check if new_node is actually new
                if new_node.get_hash_value() not in states:
                    states.add(new_node.get_hash_value())
                    queue.append(new_node)


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
    parent = boardUtils.Board()
    parent.load(sys.argv[1])

    # load cars
    cars = boardUtils.get_vehicles(parent)

    # set the row and column for which has to be ch
    if len(parent.board) % 2 == 0:
        row = (len(parent.board) / 2) - 1
    else:
        row = len(parent.board) / 2
    col = len(parent.board) - 1

    # initialize queue and states
    queue = list()
    states = set()

    # add parent to queue and states
    queue.append(parent)
    states.add(parent.get_hash_value())

start = timer()
print breadth_first_search()
end = timer()
print str(end - start) + ' seconds elapsed'