import visualisation, ast, collections, math


class Board:
    width = 0
    vehicle_index = []

    def __init__(self):
        self.vehicles = []
        self.board = []

    def load(self, string):
        """
        loads vehicles from a string
        :param string: string of board to construct vehicles from
        """
        # set class attribute
        Board.width = int(math.sqrt(len(string)))

        # populate matrix of board
        row = list()
        for index, value in enumerate(string):
            if index > 0 and index % Board.width == 0:
                self.board.append(row)
                row = list()
                row.append(value)
            else:
                row.append(value)
        self.board.append(row)

        # get the vehicles from the string
        values = collections.Counter(string)

        # get the red vehicle
        self.vehicles.append((True, string.index('?') / Board.width,
                              string.index('?') % Board.width,
                              string.rindex('?') % Board.width))
        Board.vehicle_index.append('?')
        values.pop('?')

        # add other vehicles to self.vehicles
        for identifier in values:

            # get the first and last occurrence of identifier in string
            first = string.index(identifier)
            last = string.rindex(identifier)

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


string = ast.literal_eval(raw_input('Paste the string of the board board. For example: "..abbc..a..c..a??c...eddhgge..h..eff": '))
solution = ast.literal_eval(raw_input('Paste a solution. For example: [[0,1],[1,-2]]: '))

board = Board()
board.load(string)

vis = visualisation.Visualisation(board, solution)
