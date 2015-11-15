import csv, collections
from bitarray import bitarray


class Board:
    width = 6

    def __init__(self, parent, board, cars, moved):
        self.parent = parent
        self.board = board
        self.cars = cars
        self.moved = moved

    def get_hash(self):
        return self.board.tobytes()

    def load_from_file(self, path):
        # construct board
        string_from_board = ""
        self.board = bitarray()
        with open(path) as f:
            for row in csv.reader(f):
                self.width = len(row)
                for value in row:
                    string_from_board += value

                    # bit array representation of board
                    if value == '.':
                        self.board.append(False)
                    else:
                        self.board.append(True)

        # get the cars
        self.cars = dict()
        values = collections.Counter(string_from_board)
        for name in values:
            first = string_from_board.index(name)
            last = string_from_board.rindex(name)
            if not name == '.':
                if last - first > 2:
                    self.cars[name] = ('v', first, last)
                else:
                    self.cars[name] = ('h', first, last)

    def get_moves(self):
        moves = []
        for car in self.cars:
            if self.cars[car][0] == 'h':

                # check if car can go forwards
                if not self.cars[car][1] % self.width == 0 and self.board[self.cars[car][1] - 1] == 0:
                        moves.append([car, -1])

                # check if car can go backwards
                if not (self.cars[car][2] - self.width + 1) % self.width == 0 and self.board[self.cars[car][2] + 1] == 0:
                        moves.append([car, 1])
            else:

                # check if car can go upwards
                if self.cars[car][1] >= self.width and self.board[self.cars[car][1] - self.width] == 0:
                        moves.append([car, -1])

                # check if car can go downwards
                if self.cars[car][2] < self.width * self.width - self.width and self.board[self.cars[car][2] + self.width] == 0:
                        moves.append([car, 1])

        return moves

    def move(self, car, move):
        node = Board(self, self.board[:], self.cars.copy(), (car, move))

        old = node.cars.get(car)
        update = []

        if node.cars[car][0] == 'h':
            if move > 0:
                node.board[node.cars[car][1]] = 0
                node.board[node.cars[car][2] + 1] = 1
                update.append((old[1] + 1, old[2] + 1))
            else:
                node.board[node.cars[car][1] - 1] = 1
                node.board[node.cars[car][2]] = 0
                update.append((old[1] - 1, old[2] - 1))
        else:
            if move > 0:
                node.board[node.cars[car][1]] = 0
                node.board[node.cars[car][2] + self.width] = 1
                update.append((old[1] + self.width, old[2] + self.width))
            else:
                node.board[node.cars[car][1] - self.width] = 1
                node.board[node.cars[car][2]] = 0
                update.append((old[1] - self.width, old[2] - self.width))

        # update car
        node.cars.pop(car)
        node.cars[car] = (old[0], update[0][0], update[0][1])
        return node

    def win(self):
        # TODO: remove hardcode
        return self.cars['?'][2] == 17
