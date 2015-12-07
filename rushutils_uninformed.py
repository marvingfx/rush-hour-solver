import csv, collections, math


class Board:
    # the width of the board, used in several calculations
    width = 0

    # the row of the red vehicle
    row = 0

    # list that contains the identifiers of the vehicles
    vehicle_index = list()

    def __init__(self, parent=None, board=None, vehicles=None, moved=None):
        self.parent = parent
        self.board = board
        self.vehicles = vehicles
        self.moved = moved

    def __str__(self):
        """
        returns a string of the board
        :return: string of board
        """
        string = ""
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
        self.board = []

        # read file
        with open(path) as file:
            for row in csv.reader(file):
                self.board.append(row)
                for value in row:
                    board += value

        # load vehicles
        self.vehicles = list()
        values = collections.Counter(board)

        # set class attributes
        Board.width = int(math.sqrt(len(board)))
        Board.row = int(math.floor((Board.width - 1) / 2))

        # get the red vehicle
        self.vehicles.append((True, board.index('?') / Board.width, 
                              board.index('?') % Board.width, 
                              board.rindex('?') % Board.width))
        Board.vehicle_index.append('?')
        values.pop('?')

        # get other vehicles
        for identifier in values:

            # get the first and last occurrence of identifier in string
            first = board.index(identifier)
            last = board.rindex(identifier)

            if not identifier == ".":

                # vertical vehicle
                if last - first > 2:
                    self.vehicles.append((False, first % Board.width, first / Board.width, last / Board.width))
                
                # horizontal vehicle
                else:
                    self.vehicles.append((True, first / Board.width, first % Board.width,  last % Board.width))

                # update vehicle index
                Board.vehicle_index.append(identifier)

        # update self.board to show the index of the vehicle instead of identifier
        for index, vehicle in enumerate(self.vehicles):
            
            # write index of horizontal vehicle
            if vehicle[0]:
                self.board[vehicle[1]][vehicle[2]] = index
                self.board[vehicle[1]][vehicle[3]] = index
                if vehicle[3] - vehicle[2] > 1:
                    self.board[vehicle[1]][vehicle[2] + 1] = index
                    
            # write index of vertical vehicle
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

        # update Board.width, other usages all require to subtract on from Board.width
        Board.width -= 1

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
        node = Board(self, list(self.board), list(self.vehicles), (index, move))

        vehicle = node.vehicles[index]

        # move horizontally orientated vehicle
        if vehicle[0]:
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
                node.board[vehicle[2]] = list(node.board[vehicle[2]])
                node.board[vehicle[3] + 1] = list(node.board[vehicle[3] + 1])
                node.board[vehicle[2]][vehicle[1]] = None
                node.board[vehicle[3] + 1][vehicle[1]] = index
            else:
                node.board[vehicle[2] - 1] = list(node.board[vehicle[2] - 1])
                node.board[vehicle[3]] = list(node.board[vehicle[3]])
                node.board[vehicle[2] - 1][vehicle[1]] = index
                node.board[vehicle[3]][vehicle[1]] = None
        
        # update vehicle
        node.vehicles[index] = (vehicle[0], vehicle[1], vehicle[2] + move, vehicle[3] + move)

        return node

    def win(self):
        """
        checks whether the last tile is occupied by the red vehicle
        :return: boolean which indicates a win
        """
        return self.vehicles[0][3] == Board.width
