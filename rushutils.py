import csv, collections, math


class Board:
    # the width of the board, used in several calculations
    width = 0

    # the index of the winning tile
    tile = 0

    # list that contains the identifiers of the vehicles
    vehicle_index = list()

    def __init__(self, parent=None, board=None, vehicles=None, moved=None, depth=0, value=None):
        self.parent = parent
        self.board = board
        self.vehicles = vehicles
        self.moved = moved
        self.depth = depth
        self.value = value

    def __str__(self):
        """
        returns a string of the board
        :return: string of board
        """
        string = ""

        for index, identifier in enumerate(self.board):
            if index % Board.width == 0:
                string += "\n"
            if identifier is None:
                string += "."
            else:
                string += Board.vehicle_index[identifier]

        return string

    def __lt__(self, other):
        """
        compares two Board instances on their heuristic value
        :param other:
        :return:
        """
        return self.value < other.value

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

    def load_from_file(self, path):
        """
        loads board and vehicles from a csv file
        :param path: path to file
        """
        board = ""

        # read file
        with open(path) as file:
            for row in csv.reader(file):
                for value in row:
                    board += value

        # load vehicles
        self.vehicles = list()
        values = collections.Counter(board)

        # get the red vehicle
        self.vehicles.append((True, board.index('?'), board.rindex('?')))
        Board.vehicle_index.append('?')
        values.pop('?')

        # get other vehicles
        for identifier in values:

            # get the first and last occurrence of identifier in string
            first = board.index(identifier)
            last = board.rindex(identifier)

            if not identifier == ".":

                # vertical orientated vehicle
                if last - first > 2:
                    self.vehicles.append((False, first, last))
                # horizontal orientated vehicle
                else:
                    self.vehicles.append((True, first, last))

                # update vehicle index
                Board.vehicle_index.append(identifier)

        # set class attributes
        Board.width = int(math.sqrt(len(board)))
        if Board.width % 2 == 0:
            Board.tile = (Board.width / 2 * Board.width - 1)
        else:
            Board.tile = (Board.width - 1 + int(math.floor(Board.width / 2)) * Board.width)

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

    def get_cost_estimate(self):
        """
        gets a cost estimate of the completion of the board
        :return: cost estimate
        """
        return self.depth + self.get_min_distance() + self.get_additional_steps()

    def is_blocked(self, index):
        if index is None:
            return False

        if self.vehicles[index][0]:

            # check if vehicle can go backwards
            if not self.vehicles[index][1] % Board.width == 0 and self.board[self.vehicles[index][1] - 1] is None:
                return False

            # check if vehicle can go forwards
            if not (self.vehicles[index][2] - Board.width + 1) % Board.width == 0 and self.board[self.vehicles[index][2] + 1] is None:
                return False

        else:
            # check if vehicle can go upwards
            if self.vehicles[index][1] >= Board.width and self.board[self.vehicles[index][1] - Board.width] is None:
                return False

            # check if vehicle can go downwards
            if self.vehicles[index][2] < Board.width * Board.width - Board.width and self.board[self.vehicles[index][2] + Board.width] is None:
                return False

        return True

    def get_additional_steps(self):
        """
        gets a minimum number of steps to be completed
        :return: minimum number of steps
        """
        steps = 0
        origin = self.vehicles[0][2]

        # check for vehicles in the direct path of the red vehicle
        for i in range(1, self.get_min_distance() + 1):
            index = self.board[origin + i]
            if index is not None:

                # center tile of long vehicle in path of red vehicle
                if self.vehicles[index][1] < origin and self.vehicles[index][2] > origin + i:
                    steps += 2

                # either long or short vehicle in path of red vehicle
                else:
                    steps += 1

                # check if vehicle in path can move, if not at least one step needs to be taken
                if self.is_blocked(index):
                    steps += 1

                # check if directly blocking vehicles can move
                if self.is_blocked(self.board[self.vehicles[index][1] - Board.width]) and self.is_blocked(self.board[self.vehicles[index][2] + Board.width]):
                        steps += 1

        return steps

    def get_min_distance(self):
        """
        gets the minimum distance that has to be covered by the red vehicle
        :return: minimum steps
        """
        return Board.tile - self.vehicles[0][2]

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
        :param move: direction in which the vehicle can move
        :return: new Board instance
        """

        # create new node
        node = Board(self, list(self.board), list(self.vehicles), (index, move), self.depth + 1)

        # move horizontally orientated vehicles
        if node.vehicles[index][0]:

            # update the board representation
            if move > 0:
                node.board[node.vehicles[index][1]] = None
                node.board[node.vehicles[index][2] + 1] = index
            else:
                node.board[node.vehicles[index][1] - 1] = index
                node.board[node.vehicles[index][2]] = None

            # update the vehicle
            node.vehicles[index] = (True, node.vehicles[index][1] + move, node.vehicles[index][2] + move)

        # move vertically orientated vehicles
        else:

            # update the board representation
            if move > 0:
                node.board[node.vehicles[index][1]] = None
                node.board[node.vehicles[index][2] + Board.width] = index
            else:
                node.board[node.vehicles[index][1] - Board.width] = index
                node.board[node.vehicles[index][2]] = None

            # update the vehicle
            node.vehicles[index] = (False, node.vehicles[index][1] + move * Board.width, node.vehicles[index][2] + move * Board.width)

        # get the cost estimate
        node.value = node.get_cost_estimate()

        return node

    def win(self):
        """
        checks whether the last tile is occupied by the red vehicle
        :return: boolean which indicates a win
        """
        return self.vehicles[0][2] == Board.tile
