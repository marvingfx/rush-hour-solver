import csv, collections, math
from bitarray import bitarray


class Board:
    width = 6
    winning_tile = 36

    def __init__(self, parent, board, vehicles, moved, depth = 0):
        self.parent = parent
        self.board = board
        self.vehicles = vehicles
        self.moved = moved
        self.depth = depth

    # TODO: fix issue for board3
    def get_hash(self):
        return self.board.tobytes() + str(self.depth)

    def load_from_file(self, path):
        """
        loads board and vehicles from a csv file
        :param path: path to file
        """

        # construct board
        string_from_board = ""
        self.board = bitarray()

        # read file
        with open(path) as f:
            for row in csv.reader(f):
                Board.width = len(row)
                for value in row:
                    string_from_board += value

                    # update bit array representation of board
                    if value == '.':
                        self.board.append(False)
                    else:
                        self.board.append(True)
        self.board.fill()

        # TODO: change this, it is wrong
        Board.winning_tile = int(math.floor((len(string_from_board) / 2) - 1))

        # get the vehicles
        self.vehicles = dict()
        values = collections.Counter(string_from_board)
        for name in values:
            first = string_from_board.index(name)
            last = string_from_board.rindex(name)
            if not name == '.':

                # add vehicle to dictionary
                if last - first > 2:
                    self.vehicles[name] = ('v', first, last)
                else:
                    self.vehicles[name] = ('h', first, last)

    def get_moves(self):
        """
        checks which vehicles can move
        :return: array with possible moves
        """
        moves = []
        for vehicle in self.vehicles:
            if self.vehicles[vehicle][0] == 'h':

                # check if vehicle can go forwards
                if not self.vehicles[vehicle][1] % self.width == 0 and self.board[self.vehicles[vehicle][1] - 1] == 0:
                        moves.append([vehicle, -1])

                # check if vehicle can go backwards
                if not (self.vehicles[vehicle][2] - self.width + 1) % self.width == 0 and self.board[self.vehicles[vehicle][2] + 1] == 0:
                        moves.append([vehicle, 1])
            else:

                # check if vehicle can go upwards
                if self.vehicles[vehicle][1] >= self.width and self.board[self.vehicles[vehicle][1] - self.width] == 0:
                        moves.append([vehicle, -1])

                # check if vehicle can go downwards
                if self.vehicles[vehicle][2] < self.width * self.width - self.width and self.board[self.vehicles[vehicle][2] + self.width] == 0:
                        moves.append([vehicle, 1])

        return moves

    def move(self, vehicle, move):
        """
        moves the vehicle on the board
        :param vehicle: id of vehicle that can be moved
        :param move: direction in which the car can move
        :return: new Board instance
        """

        # create new node
        node = Board(self, self.board[:], self.vehicles.copy(), (vehicle, move))

        old = node.vehicles.pop(vehicle)

        # initialize variables
        first = old[1]
        last = old[2]
        update = []

        # move horizontally orientated cars
        if old[0] == 'h':
            if move > 0:
                node.board[first] = 0
                node.board[last + 1] = 1
                update.append((first + 1, last + 1))
            else:
                node.board[first - 1] = 1
                node.board[last] = 0
                update.append((first - 1, last - 1))

        # move vertically orientated cars
        else:
            if move > 0:
                node.board[first] = 0
                node.board[last + self.width] = 1
                update.append((first + self.width, last + self.width))
            else:
                node.board[first - self.width] = 1
                node.board[last] = 0
                update.append((first - self.width, last - self.width))

        # update vehicle dictionary
        node.vehicles[vehicle] = (old[0], update[0][0], update[0][1])

        return node

    def win(self):
        return self.vehicles['?'][2] == 44
