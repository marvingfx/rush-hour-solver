import csv, collections, math


class Board:
    # the width of the board, used in several calculations
    width = 0

    # the row of the red vehicle
    row = 0

    # list that contains the identifiers of the vehicles, used to print a node
    vehicle_index = list()

    def __init__(self, board=None, vehicles=None, moved=None, depth=0, value=None):
        self.board = board
        self.vehicles = vehicles
        self.moved = moved
        self.depth = depth
        self.value = value

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
        node = Board(list(self.board), list(self.vehicles), (index, move), self.depth + 1)

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

        # calculate the cost estimate
        node.value = node.get_cost_estimate()

        return node

    def get_cost_estimate(self):
        """
        gets a cost estimate of the completion of the board
        :return: cost estimate
        """
        return self.depth + self.get_min_distance() + self.get_additional_steps()

    def get_min_distance(self):
        """
        gets the minimum distance that has to be covered by the red vehicle
        :return: minimum steps
        """
        return Board.width - self.vehicles[0][3]

    def get_additional_steps(self):
        """
        calculates a minimum number of steps that need to be done before completing the board
        :return: minimum number of steps
        """
        steps = 0
        origin = self.vehicles[0][3]

        # check for vehicles in the direct path of the red vehicle
        for i in range(1, self.get_min_distance() + 1):

            # get the i places from the red vehicle
            index = self.board[Board.row][origin + i]

            if index:

                # get the directly blocking vehicle
                vehicle = self.vehicles[index]

                # center tile of long vehicle in path of red vehicle (1st level blocker)
                if vehicle[2] < self.vehicles[0][1] < vehicle[3]:
                    steps += 2

                    # check if 1st level blocker is blocked on both sides (2nd level blocker)
                    if self.is_blocked(index):
                        steps += 1

                        # check if 2nd level blockers are blocked on both sides (3d level blocker)
                        if self.is_blocked(self.board[vehicle[2] - 1][vehicle[1]]) and self.is_blocked(self.board[vehicle[3] + 1][vehicle[1]]):
                            steps += 1

                # either long or short vehicle in path of red vehicle (1st level blocker)
                else:
                    steps += 1

                    # check if 1st level blocker is blocked on both sides (2nd level blocker)
                    if self.is_blocked(index):
                        steps += 1

                        # check if 2nd level blockers are blocked on both sides (3d level blocker)
                        if self.is_blocked(self.board[vehicle[2] - 1][vehicle[1]]) and self.is_blocked(self.board[vehicle[3] + 1][vehicle[1]]):
                            steps += 1

                    # check if 1st level blocker's shortest route is blocked (2nd level blocker)
                    elif vehicle[2] == self.vehicles[0][1]:
                        if self.is_blocked(self.board[vehicle[3] + 1][vehicle[1]]) and self.board[vehicle[2] - 2][vehicle[1]]:
                            steps += 2
                        elif self.board[vehicle[3] + 1][vehicle[1]]:
                            steps += 1

                    # check if 1st level blocker's shortest route is blocked (2nd level blocker)
                    else:
                        if self.is_blocked(self.board[vehicle[2] - 1][vehicle[1]]) and self.board[vehicle[3] + 2][vehicle[1]]:
                            steps += 2
                        elif self.board[vehicle[2] - 1][vehicle[1]]:
                            steps += 1

        return steps

    def is_blocked(self, index):
        """
        checks whether is blocked
        :param index: index of the vehicle
        :return: boolean indicating if vehicle is blocked
        """
        if not index:
            return False

        #
        vehicle = self.vehicles[index]

        # horizontally orientated vehicle
        if vehicle[0]:
            if vehicle[2] == 0 and self.board[vehicle[1]][vehicle[2] - 1]:
                return True
            elif vehicle[3] == Board.width and self.board[vehicle[1]][vehicle[2] - 1]:
                return True
            elif self.board[vehicle[1]][vehicle[2] - 1] and self.board[vehicle[1]][vehicle[3] + 1]:
                return True

        # vertically orientated vehicle
        else:
            if vehicle[2] == 0 and self.board[vehicle[3] + 1][vehicle[1]]:
                return True
            elif vehicle[3] == Board.width and self.board[vehicle[2] - 1][vehicle[1]]:
                return True
            elif self.board[vehicle[2] - 1][vehicle[1]] and self.board[vehicle[3] + 1][vehicle[1]]:
                return True

        return False
