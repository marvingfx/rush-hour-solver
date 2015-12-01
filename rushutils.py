import csv, collections, math
from bitarray import bitarray


class Board:
    width = 0
    tile = 0
    vehicle_index = list()

    def __init__(self, parent=None, board=None, vehicles=None, moved=None, depth=0, value=None):
        self.parent = parent
        self.board = board
        self.vehicles = vehicles
        self.moved = moved
        self.depth = depth
        self.value = value

    def __str__(self):
        string = ""
        for index, identifier in enumerate(self.board):
            if index % Board.width == 0:
                string += "\n"
            if identifier is None:
                string += "."
            else:
                string += Board.vehicle_index[identifier]
        return string

    def get_hash(self):
        """
        gets a hashable value
        :return: tuple of self.vehicles
        """
        return tuple(self.vehicles)

    """ may be implemented later
    def __hash__(self):
        return hash(tuple(self.vehicles))

    def __eq__(self, other):
        return self.vehicles == other.vehicles
    """

    def __lt__(self, other):
        """
        compares two Board instances on their heuristic value
        :param other:
        :return:
        """
        return self.value < other.value

    def get_value(self):
        """
        gets the heuristic value of the current board
        :return: heuristic value
        """
        return self.depth + self.get_min_distance() + self.get_additional_steps()

    def get_additional_steps(self):
        """
        gets a minimum number of vehicles that need to be moved
        :return: minimum number of vehicles
        """

        steps = 0
        origin = self.vehicles[0][2]

        # check for vehicles in the direct path of the red vehicle
        for i in range(1, self.get_min_distance() + 1):
            if self.board[origin + i] is not None:

                # long vehicle (3 tiles, center tile in path of red vehicle)
                if self.board[origin + i - Board.width] == self.board[origin + i + Board.width]:
                    steps += 2
                    if self.board[origin + i - Board.width * 2] is not None and self.board[origin + i + Board.width * 2] is not None:
                        steps += 2

                # long vehicle (3 tiles, bottom tile in path of red vehicle)
                elif self.board[origin + i] == self.board[origin + i - Board.width * 2]:
                    steps += 1
                    if self.board[origin + i - Board.width * 3] is not None and self.board[origin + i + Board.width] is not None:
                        steps += 2

                # long vehicle (3 tiles, top tile in path of red vehicle)
                elif self.board[origin + i] == self.board[origin + i - Board.width * 2]:
                    steps += 1
                    if self.board[origin + i + Board.width * 3] is not None and self.board[origin + i - Board.width] is not None:
                        steps += 2

                # short vehicle (2 tiles, bottom tile in path of red vehicle)
                elif self.board[origin + i - Board.width] == self.board[origin + i]:
                    steps += 1
                    if self.board[origin + i - Board.width * 2] is not None and self.board[origin + i + Board.width] is not None:
                        steps += 2

                # short vehicle (2 tiles, top tile in path of red vehicle)
                else:
                    steps += 1
                    if self.board[origin + i + Board.width * 2] is not None and self.board[origin + i - Board.width] is not None:
                        steps += 2

        return steps

    def get_min_distance(self):
        """
        gets the minimum distance that has to be covered by the red vehicle
        :return: minimum steps
        """
        return Board.tile - self.vehicles[0][2]

    def load_from_file(self, path):
        """
        loads board and vehicles from a csv file
        :param path: path to file
        """

        # construct board
        board = ""

        # read file
        with open(path) as file:
            for row in csv.reader(file):
                for value in row:
                    board += value

        # set class attributes
        Board.width = int(math.sqrt(len(board)))
        if Board.width % 2 == 0:
            Board.tile = (Board.width / 2 * Board.width - 1)
        else:
            Board.tile = (Board.width - 1 + int(math.floor(Board.width / 2)) * Board.width)

        # load vehicles
        self.vehicles = list()
        values = collections.Counter(board)

        # get the red vehicle first
        self.vehicles.append((True, board.index('?'), board.rindex('?')))
        Board.vehicle_index.append('?')
        values.pop('?')

        # get other vehicles
        for identifier in values:
            first = board.index(identifier)
            last = board.rindex(identifier)
            if not identifier == ".":

                if last - first > 2:
                    self.vehicles.append((False, first, last))
                else:
                    self.vehicles.append((True, first, last))

                Board.vehicle_index.append(identifier)

        self.board = list(board)
        for index, vehicle in enumerate(self.vehicles):
            self.board[vehicle[1]] = index
            self.board[vehicle[2]] = index
            if vehicle[0]:
                if vehicle[2] - vehicle[1] > 1:
                    self.board[vehicle[1] + 1] = index
            else:
                if vehicle[2] - vehicle[1] > Board.width:
                    self.board[vehicle[1] + Board.width] = index

        for index, value in enumerate(self.board):
            if value == ".":
                self.board[index] = None

    def get_moves(self):
        """
        checks which vehicles can move
        :return: array with possible moves
        """
        moves = []
        for index, vehicle in enumerate(self.vehicles):

            # horizontally orientated vehicle
            if vehicle[0]:

                # check if vehicle can go backwards
                if not vehicle[1] % Board.width == 0 and self.board[vehicle[1] - 1] is None:
                    moves.append([index, -1])

                # check if vehicle can go forwards
                if not (vehicle[2] - Board.width + 1) % Board.width == 0 and self.board[vehicle[2] + 1] is None:
                    moves.append([index, 1])

            # vertically orientated vehicle
            else:

                # check if vehicle can go upwards
                if vehicle[1] >= Board.width and self.board[vehicle[1] - Board.width] is None:
                    moves.append([index, -1])

                # check if vehicle can go downwards
                if vehicle[2] < Board.width * Board.width - Board.width and self.board[vehicle[2] + Board.width] is None:
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
        first = old[1]
        last = old[2]

        # move horizontally orientated vehicles
        if old[0]:
            if move > 0:
                node.board[first] = None
                node.board[last + 1] = index
                update.append((first + 1, last + 1))
            else:
                node.board[first - 1] = index
                node.board[last] = None
                update.append((first - 1, last - 1))

        # move vertically orientated vehicles
        else:
            if move > 0:
                node.board[first] = None
                node.board[last + Board.width] = index
                update.append((first + Board.width, last + Board.width))
            else:
                node.board[first - Board.width] = index
                node.board[last] = None
                update.append((first - Board.width, last - Board.width))

        node.vehicles[index] = (old[0], update[0][0], update[0][1])
        node.value = node.get_value()
        return node

    def win(self):
        """
        checks whether the last tile is occupied by the red vehicle
        :return: boolean which indicates a win
        """
        return self.vehicles[0][2] == Board.tile
