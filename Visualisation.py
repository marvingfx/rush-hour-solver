import pygame, math, random, sys
from pygame.locals import *
from collections import Counter

# hardcode, to be removed
WIDTH = 480
TILE = 80
board = list("..abbc..a..c..a??c...eddhgge..h..eff")
bwidth = int(math.sqrt(len(board)))
vehicles = [('?', True, 15, 16), ('a', False, 2, 14), ('c', False, 5, 17), ('b', True, 3, 4), ('e', False, 21, 33), ('d', True, 22, 23), ('g', True, 25, 26), ('f', True, 34, 35), ('h', False, 24, 30)]
solution = [(1, 1), (3, -1), (3, -1), (8, -1), (8, -1), (6, -1), (1, 1), (1, 1), (0, -1), (0, -1), (4, -1), (4, -1), (4, -1), (5, -1), (2, 1), (2, 1), (7, -1), (2, 1), (8, -1), (8, -1), (0, -1), (1, -1), (1, -1), (6, 1), (6, 1), (6, 1), (1, 1), (1, 1), (0, 1), (8, 1), (3, -1), (8, 1), (8, 1), (0, -1), (1, -1), (1, -1), (1, -1), (5, -1), (5, -1), (4, 1), (7, -1), (7, -1), (8, 1), (5, -1), (1, 1), (3, 1), (3, 1), (3, 1), (1, -1), (3, 1), (4, -1), (5, 1), (5, 1), (5, 1), (1, 1), (1, 1), (8, -1), (7, -1), (1, 1), (0, 1), (8, -1), (8, -1), (8, -1), (0, -1), (1, -1), (1, -1), (1, -1), (5, -1), (5, -1), (4, 1), (5, -1), (1, 1), (6, -1), (6, -1), (4, 1), (4, 1), (6, -1), (1, 1), (1, 1), (0, 1), (0, 1), (0, 1), (0, 1)]
colorlist = Counter(board)

# assigns a random color to each vehicle
for vehicle in colorlist:
    if not vehicle == '?':
        colorlist[vehicle] = (int(random.random() * 256), int(random.random() * 256), int(random.random() * 256))

# assign red color to main vehicle
colorlist['?'] = (255, 0, 0)

def update_board(move):
    """
    updates the list representation of the board
    :param move: tuple containing the index of the vehicle and the movement
    """
    vehicle = vehicles[move[0]]
    if vehicle[1]:
        # move right
        if move[1] > 0:
            board[vehicle[3] + 1] = vehicle[0]
            board[vehicle[2]] = '.'
        # move left
        else:
            board[vehicle[2] - 1] = vehicle[0]
            board[vehicle[3]] = '.'
        vehicles[move[0]] = (vehicle[0], vehicle[1], vehicle[2] + move[1], vehicle[3] + move[1])

    else:
        # move down
        if move[1] > 0:
            board[vehicle[3] + bwidth] = vehicle[0]
            board[vehicle[2]] = '.'
        # move up
        else:
            board[vehicle[2] - bwidth] = vehicle[0]
            board[vehicle[3]] = '.'
        vehicles[move[0]] = (vehicle[0], vehicle[1], vehicle[2] + (move[1] * bwidth), vehicle[3] + (move[1] * bwidth))

def draw_board():
    """
    draws the current board on the window
    """
    for index, tile in enumerate(board):
        if not tile == '.':
             pygame.draw.rect(window, colorlist[tile], ((index % bwidth) * TILE, (index / bwidth) * TILE, TILE, TILE))

def exit():
    """
    quits the current program
    """
    pygame.quit()
    sys.exit()

def pause():
    """
    pauses the game, waits for input from user
    """
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            break

def check_pause():
    """
    checks if a button is pressed
    """

    # quit program
    for event in pygame.event.get(QUIT):
        exit()

    # pause program
    for event in pygame.event.get(KEYDOWN):
        pause()

# actual visualisation
pygame.init()
window = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Rush Hour')
window.fill((255, 255, 255))
draw_board()
pygame.display.update()

# pause the game so that it doesn't start automatically
pause()

# iterate over the moves in the solution
while len(solution) > 0:
    check_pause()
    window.fill((255, 255, 255))
    update_board(solution.pop(0))
    draw_board()
    pygame.display.update()
    pygame.time.wait(150)

# wait for input to quit the game
while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        exit()
    if event.type == KEYDOWN:
        exit()
