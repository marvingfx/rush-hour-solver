import visualisation, ast, collections, math


class Board:
    width = 0
    vehicle_index = []


    def __init__(self):
        self.vehicles = None
        self.board = None

    def load(self, string):
        self.vehicles = list()

        values = collections.Counter(string)

        Board.width = int(math.sqrt(len(string)))

        self.board = []
        row = list()
        for index, value in enumerate(string):
            if index > 0 and index % Board.width == 0:
                self.board.append(row)
                row = list()
                row.append(value)
            else:
                row.append(value)
        self.board.append(row)

        # get the red vehicle
        self.vehicles.append((True, string.index('?') / Board.width,
                              string.index('?') % Board.width,
                              string.rindex('?') % Board.width))
        Board.vehicle_index.append('?')
        values.pop('?')

        # get other vehicles
        for identifier in values:

            # get the first and last occurrence of identifier in string
            first = string.index(identifier)
            last = string.rindex(identifier)

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

        Board.width -= 1


string = ast.literal_eval(raw_input('Paste the string of the board board. For example: "..abbc..a..c..a??c...eddhgge..h..eff": '))
solution = ast.literal_eval(raw_input('Paste a solution. For example: [[0,1],[1,-2]]: '))

board = Board()
board.load(string)

vis = visualisation.Visualisation(board, solution)