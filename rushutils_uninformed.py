import csv, collections, math


class Board:
    # the width of the board, used in several calculations
    width = 0

    # the row of the red vehicle
    row = 0

    # list that contains the identifiers of the vehicles, used to print a node
    vehicle_index = list()

    def __init__(self, board=None, vehicles=None, moved=None):
        self.board = board
        self.vehicles = vehicles
        self.moved = moved

    def __str__(self):
        """
        returns a string representation of the board
        :return: string of board
        """
        string = ""

        # transform matrix into string
        for row in self.board:
            for value in row:
                if value is None:
                    string += "."
                else:
                    string += self.vehicle_index[value]
            string += "\n"

        return string

    def __lt__(self, other):
        """
        compares two Board instances on their cost
        :param other:
        :return:
        """
        return self.value < other.value

    def get_hash(self):
        """
        gets a value that is used to save nodes
        __hash__ will store a reference to a tuple/board while get_hash() will store the actual tuple, which in turn
        leads to less memory usage
        :return self.vehicles (tuple):
        """
        return self.vehicles

    def load_from_file(self, path):
        """
        loads board and vehicles from a csv file
        :param path: path to file
        """
        board = ""
        self.board = []

        # read file and populate matrix
        with open(path) as file:
            for row in csv.reader(file):
                self.board.append(row)
                for value in row:
                    board += value

        # set class attributes
        Board.width = int(math.sqrt(len(board)))
        Board.row = int(math.floor((Board.width - 1) / 2))

        # get the vehicles from the string
        self.vehicles = list()
        values = collections.Counter(board)

        # add main vehicle to self.vehicles
        self.vehicles.append((True, board.index('?') / Board.width,
                              board.index('?') % Board.width,
                              board.rindex('?') % Board.width))

        # add main vehicle identifier to Board.vehicle_index
        Board.vehicle_index.append('?')
        values.pop('?')

        # add other vehicles to self.vehicles
        for identifier in values:

            # get the first and last occurrence of identifier in string
            first = board.index(identifier)
            last = board.rindex(identifier)

            if not identifier == ".":

                # vertical vehicle: (vertical, column, first row, last row)
                if last - first > 2:
                    self.vehicles.append((False, first % Board.width, first / Board.width, last / Board.width))

                # horizontal vehicle: (horizontal, row, first column, last column)
                else:
                    self.vehicles.append((True, first / Board.width, first % Board.width,  last % Board.width))

                # add vehicle to Board.vehicle_index
                Board.vehicle_index.append(identifier)

        # transform list to tuple for hashing
        self.vehicles = tuple(self.vehicles)

        # update self.board to use the index of the vehicle instead of identifier
        for index, vehicle in enumerate(self.vehicles):

            # write indexes of horizontal vehicle
            if vehicle[0]:
                self.board[vehicle[1]][vehicle[2]] = index
                self.board[vehicle[1]][vehicle[3]] = index
                if vehicle[3] - vehicle[2] > 1:
                    self.board[vehicle[1]][vehicle[2] + 1] = index

            # write indexes of vertical vehicle
            else:
                self.board[vehicle[2]][vehicle[1]] = index
                self.board[vehicle[3]][vehicle[1]] = index
                if vehicle[3] - vehicle[2] > 1:
                    self.board[vehicle[2] + 1][vehicle[1]] = index

        # replace '.' with None
        for row in range(Board.width):
            for col in range(Board.width):
                if self.board[row][col] == ".":
                    self.board[row][col] = None

        # update Board.width, other usages all require to subtract one from Board.width
        Board.width -= 1

    def win(self):
        """
        checks whether the last tile is occupied by the red vehicle
        :return: boolean which indicates a win
        """
        return self.vehicles[0][3] == Board.width

    def get_moves(self):
        """
        checks which vehicles can move
        :return: array with all possible moves
        """
        moves = []
        for index, vehicle in enumerate(self.vehicles):

            # horizontally orientated vehicle
            if vehicle[0]:

                # check if vehicle can go backwards
                if not vehicle[2] == 0 and self.board[vehicle[1]][vehicle[2] - 1] is None:
                    moves.append([index, -1])

                # check if vehicle can go forwards
                if not vehicle[3] == Board.width and self.board[vehicle[1]][vehicle[3] + 1] is None:
                    moves.append([index, 1])

            # vertically orientated vehicle
            else:

                # check if vehicle can go upwards
                if not vehicle[2] == 0 and self.board[vehicle[2] - 1][vehicle[1]] is None:
                    moves.append([index, -1])

                # check if vehicle can go downwards
                if not vehicle[3] == Board.width and self.board[vehicle[3] + 1][vehicle[1]] is None:
                    moves.append([index, 1])

        return moves

    def move(self, index, move):
        """
        moves the vehicle on the board
        :param index: index of vehicle that can be moved
        :param move: direction in which the vehicle can move
        :return: new Board instance
        """

        # create new node
        node = Board(list(self.board), list(self.vehicles), (index, move))

        # get the vehicle that needs to be moved
        vehicle = node.vehicles[index]

        # move horizontally orientated vehicle
        if vehicle[0]:

            # generate new row for board
            node.board[vehicle[1]] = list(node.board[vehicle[1]])

            if move > 0:
                node.board[vehicle[1]][vehicle[2]] = None
                node.board[vehicle[1]][vehicle[3] + 1] = index
            else:
                node.board[vehicle[1]][vehicle[2] - 1] = index
                node.board[vehicle[1]][vehicle[3]] = None

        # move vertically orientated vehicle
        else:
            if move > 0:

                # generate new rows for board
                node.board[vehicle[2]] = list(node.board[vehicle[2]])
                node.board[vehicle[3] + 1] = list(node.board[vehicle[3] + 1])

                node.board[vehicle[2]][vehicle[1]] = None
                node.board[vehicle[3] + 1][vehicle[1]] = index
            else:

                # generate new rows for board
                node.board[vehicle[2] - 1] = list(node.board[vehicle[2] - 1])
                node.board[vehicle[3]] = list(node.board[vehicle[3]])

                node.board[vehicle[2] - 1][vehicle[1]] = index
                node.board[vehicle[3]][vehicle[1]] = None

        # update node.vehicles
        node.vehicles[index] = (vehicle[0], vehicle[1], vehicle[2] + move, vehicle[3] + move)
        node.vehicles = tuple(node.vehicles)

        return node
