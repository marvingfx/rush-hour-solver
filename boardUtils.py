class Board:
    def __init__(self):
        self.id = "testing"

class Car:
    def __init__(self, id, index, orientation, length):
        self.id = id
        self.index = index
        self.orientation = orientation
        self.length = length

    def __eq__(self, other):
        return self.id == other

    def __str__(self):
        return self.id + ' length:' + str(self.length) + ' orientation:' + self.orientation + ' row or col:' + str(self.index)

    def getMoves(self, board):
        # checks horizontally orientated cars
        if self.orientation == 'h':
            row = board[self.index]
            try:
                left = row.index(self.id)
                right = left + self.length - 1
                moves = []
                if row[left-1] == '.' and not left == 0:
                    moves.append(-1)
                if row[right + 1] == '.' and not right == len(board):
                    moves.append(1)
            except:
                return moves
            return moves

        # checks vertically orientated cars
        elif self.orientation == 'v':
            col = [row[self.index] for row in board]
            print col
            try:
                top = col.index(self.id)
                bottom = top + self.length - 1
                moves = []
                if col[top - 1] == '.' and not top == 0:
                    moves.append(-1)
                if col[bottom + 1] == '.' and not bottom == len(board):
                    moves.append(1)
            except:
                return moves
            return moves

    # Creates a new board / node
    def move(self, number, board):
        return board

# gets the cars from the board
def getCars(board):

    # count occurances of letters
    occurances = []
    for line in board:
        for block in line:
            if not block == '.':
                occurances.append(block)
    lengths = {car:occurances.count(car) for car in occurances}

    # get horizontal cars
    hor = []
    currentCar = line[0][0]
    for line in board:
        for block in line:
            if not block == '.' and currentCar == block:
                if block not in hor:
                    hor.append(Car(block, board.index(line), 'h', lengths[block]))
                    lengths.pop(block)
            currentCar = block

    # get vertical cars
    ver = []
    for id in list(set(lengths)):
        for i in range(len(board)-1):
            col = [row[i] for row in board]
            if id in col:
                ver.append(Car(id, i, 'v', lengths[str(id)]))

    # combine lists
    return hor + ver