import csv, collections, math
from bitarray import bitarray


class Board:
    width = 0
    tile = 0

    def __init__(self, parent=None, board=None, vehicles=None, moved=None, depth=0):
        self.parent = parent
        self.board = board
        self.vehicles = vehicles
        self.moved = moved
        self.depth = depth

    def get_hash(self):
        return tuple(self.vehicles)

    """ may be implemented later
    def __hash__(self):
        return hash(tuple(self.vehicles))

    def __eq__(self, other):
        return self.vehicles == other.vehicles
    """

    def load_from_file(self, path):
        """
        loads board and vehicles from a csv file
        :param path: path to file
        """

        # construct board
        string_from_board = ""
        self.board = bitarray()

        # read file
        with open(path) as file:
            for row in csv.reader(file):
                for value in row:
                    string_from_board += value

                    # update bit array representation of board
                    if value == '.':
                        self.board.append(False)
                    else:
                        self.board.append(True)

        # set class attributes
        Board.width = int(math.sqrt(len(string_from_board)))
        if Board.width % 2 == 0:
            Board.tile = (Board.width / 2 * Board.width - 1)
        else:
            Board.tile = (Board.width - 1 + int(math.floor(Board.width / 2)) * Board.width)

        # load vehicles
        self.vehicles = list()
        values = collections.Counter(string_from_board)

        # get the red vehicle first
        self.vehicles.append(('?', True, string_from_board.index('?'), string_from_board.rindex('?')))
        values.pop('?')

        # get other vehicles
        for name in values:
            first = string_from_board.index(name)
            last = string_from_board.rindex(name)
            if not name == '.':

                # add vehicle to list
                if last - first > 2:
                    self.vehicles.append((name, False, first, last))
                else:
                    self.vehicles.append((name, True, first, last))

    def get_moves(self):
        """
        checks which vehicles can move
        :return: array with possible moves
        """
        moves = []
        for index, vehicle in enumerate(self.vehicles):

            if vehicle[1]:

                # check if vehicle can go backwards
                if not vehicle[2] % Board.width == 0 and self.board[vehicle[2] - 1] == 0:
                        moves.append([index, -1])

                # check if vehicle can go forwards
                if not (vehicle[3] - Board.width + 1) % Board.width == 0 and self.board[vehicle[3] + 1] == 0:
                        moves.append([index, 1])

            else:

                # check if vehicle can go upwards
                if vehicle[2] >= Board.width and self.board[vehicle[2] - Board.width] == 0:
                        moves.append([index, -1])

                # check if vehicle can go downwards
                if vehicle[3] < Board.width * Board.width - Board.width and self.board[vehicle[3] + Board.width] == 0:
                        moves.append([index, 1])

        return moves

    def move(self, index, move):
        """
        moves the vehicle on the board
        :param index: index of vehicle that can be moved
        :param move: direction in which the car can move
        :return: new Board instance
        """

        # create new node
        node = Board(self, list(self.board), list(self.vehicles), (index, move), self.depth + 1)
        update = []
        old = node.vehicles[index]

        # initialize variables
        first = old[2]
        last = old[3]

        # move horizontally orientated vehicles
        if old[1]:
            if move > 0:
                node.board[first] = 0
                node.board[last + 1] = 1
                update.append((first + 1, last + 1))
            else:
                node.board[first - 1] = 1
                node.board[last] = 0
                update.append((first - 1, last - 1))

        # move vertically orientated vehicles
        else:
            if move > 0:
                node.board[first] = 0
                node.board[last + Board.width] = 1
                update.append((first + Board.width, last + Board.width))
            else:
                node.board[first - Board.width] = 1
                node.board[last] = 0
                update.append((first - Board.width, last - Board.width))

        # update vehicle dictionary
        node.vehicles[index] = (old[0], old[1], update[0][0], update[0][1])
        return node

    def win(self):
        return self.vehicles[0][3] == Board.tile
