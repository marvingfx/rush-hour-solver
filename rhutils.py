import csv
import collections


class Board:
    def __init__(self, node, move, depth):
        if node:
            self.board = [row[:] for row in node.board]
        else:
            self.board = []
        self.parent = node
        self.move = move
        self.depth = depth

    def __str__(self):
        board_as_string = ''
        for row in self.board:
            for tile in row:
                board_as_string += str(tile) + '\t'
            board_as_string += '\n'
        return board_as_string

    def get_hash_value(self):
        return str(self.board)

    def load_from_file(self, path):
        with open(path) as f:
            for row in csv.reader(f):
                int_row = []
                for value in row:
                    int_row.append(int(value))
                self.board.append(int_row)


class Vehicle:
    def __init__(self, id, index, orientation, length):
        self.id = id
        self.index = index
        self.orientation = orientation
        self.length = length

    def __eq__(self, other):
        return self.id == other

    def __str__(self):
        return str(self.id) + ' length:' + str(self.length) + ' orientation:' + self.orientation + ' row or col:' + str(self.index)

    def get_moves(self, node):
        """
        gets the possible moves from current node
        :param node: node node
        :return: list with possible moves
        """
        # checks horizontally orientated vehicles
        if self.orientation == 'h':
            # gets the row in which the vehicle is located
            row = node.board[self.index]
            # see if vehicle can move by one
            try:
                left = row.index(self.id)
                right = left + self.length - 1
                moves = []
                if row[left-1] == 0 and not left == 0:
                    moves.append(-1)
                if row[right + 1] == 0 and not right == len(node.board) - 1:
                    moves.append(1)
            except:
                return moves

        # checks vertically orientated vehicles
        elif self.orientation == 'v':
            # gets the column in which the vehicle is located
            col = [row[self.index] for row in node.board]
            # see if vehicle can move by one
            try:
                top = col.index(self.id)
                bottom = top + self.length - 1
                moves = []
                if col[top - 1] == 0 and not top == 0:
                    moves.append(-1)
                if col[bottom + 1] == 0 and not bottom == len(node.board) - 1:
                    moves.append(1)
            except:
                return moves

        # return an list with possible moves
        return moves

    def move(self, number, node):
        """
        updates the board by moving a vehicle
        :param number: number to move
        :param node: node
        """

        if self.orientation == 'h':
            row = node.board[self.index]
            if number > 0:
                row[row.index(self.id) + self.length] = self.id
                row[row.index(self.id)] = 0
            else:
                row[row.index(self.id) - 1] = self.id
                row[row.index(self.id) + self.length] = 0
            node.board[self.index] = row

        elif self.orientation == 'v':
            col = [row[self.index] for row in node.board]
            if number > 0:
                col[col.index(self.id) + self.length] = self.id
                col[col.index(self.id)] = 0
            else:
                col[col.index(self.id) - 1] = self.id
                col[col.index(self.id) + self.length] = 0

            for index, row in enumerate(node.board):
                row[self.index] = col[index]


def get_vehicles(node):
    """
    creates a list of vehicle objects from a board
    :param node: node
    :return: list with vehicle objects
    """

    # count occurances of letters
    occurances = []
    for row in node.board:
        for item in row:
            if not item == 0:
                occurances.append(item)
    lengths = {car: occurances.count(car) for car in occurances}

    # get horizontal cars
    hor = []
    for row in node.board:
        duplicates = [vehicle for vehicle, count in collections.Counter(row).items() if count > 1 and not vehicle == 0]
        for vehicle in duplicates:
            if vehicle not in hor:
                hor.append(Vehicle(vehicle, node.board.index(row), 'h', lengths.get(vehicle)))
                lengths.pop(vehicle)

    # get vertical cars
    ver = []
    for item in lengths:
        for i in range(len(node.board)):
            col = [row[i] for row in node.board]
            if item in col:
                ver.append(Vehicle(item, i, 'v', lengths[item]))

    # combine lists
    return hor + ver