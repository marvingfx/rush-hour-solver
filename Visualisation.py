import pygame, csv, math, random, sys
from pygame.locals import *
from collections import Counter

WIDTH = 480
TILE = 80
FPS = 30

# hardcode, to be removed
board = list("..abbc..a..c..a??c...eddhgge..h..eff")
bwidth = int(math.sqrt(len(board)))
vehicles = [('?', True, 15, 16), ('a', False, 2, 14), ('c', False, 5, 17), ('b', True, 3, 4), ('e', False, 21, 33), ('d', True, 22, 23), ('g', True, 25, 26), ('f', True, 34, 35), ('h', False, 24, 30)]
solution = [(1, 1), (3, -1), (3, -1), (8, -1), (8, -1), (6, -1), (1, 1), (1, 1), (0, -1), (0, -1), (4, -1), (4, -1), (4, -1), (5, -1), (2, 1), (2, 1), (7, -1), (2, 1), (8, -1), (8, -1), (0, -1), (1, -1), (1, -1), (6, 1), (6, 1), (6, 1), (1, 1), (1, 1), (0, 1), (8, 1), (3, -1), (8, 1), (8, 1), (0, -1), (1, -1), (1, -1), (1, -1), (5, -1), (5, -1), (4, 1), (7, -1), (7, -1), (8, 1), (5, -1), (1, 1), (3, 1), (3, 1), (3, 1), (1, -1), (3, 1), (4, -1), (5, 1), (5, 1), (5, 1), (1, 1), (1, 1), (8, -1), (7, -1), (1, 1), (0, 1), (8, -1), (8, -1), (8, -1), (0, -1), (1, -1), (1, -1), (1, -1), (5, -1), (5, -1), (4, 1), (5, -1), (1, 1), (6, -1), (6, -1), (4, 1), (4, 1), (6, -1), (1, 1), (1, 1), (0, 1), (0, 1), (0, 1), (0, 1)]
colorlist = Counter(board)
for vehicle in colorlist:
    if not vehicle == '?':
        colorlist[vehicle] = (int(random.random()*255),int(random.random()*255),int(random.random()*255))
colorlist['?'] = (255, 0, 0)

def update_board(move):
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
    for index, tile in enumerate(board):
        if not tile == '.':
             pygame.draw.rect(window, colorlist[tile], ((index % bwidth) * 80, (index / bwidth) * 80, 80, 80))

def exit():
    pygame.quit()
    sys.exit()

def pause():
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            break

def check_pause():
    for event in pygame.event.get(QUIT):
        exit()
    for event in pygame.event.get(KEYDOWN):
        pause()

# actual visualisation
pygame.init()
window = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Rush Hour')
window.fill((255, 255, 255))
draw_board()
pygame.display.update()

pause()

while len(solution) > 0:
    check_pause()
    window.fill((255, 255, 255))
    update_board(solution.pop(0))
    draw_board()
    pygame.display.update()
    pygame.time.wait(150)

# wait for input
while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        exit()
    if event.type == KEYDOWN:
        exit()
