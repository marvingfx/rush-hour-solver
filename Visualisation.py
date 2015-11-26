import pygame
import sys
import random
from pygame.locals import *

# Create the board.
# Number of columns.
BOARDWIDTH = 6
# Number of rows.
BOARDHEIGHT = 6
TILESIZE = 80
WINDOWWIDTH = 480
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

# Colors  R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_BLUE = (0, 50, 255)
DARK_TURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)
GREY = (224, 224, 224)

BACKGROUND_COLOR = DARK_TURQUOISE
TILE_COLOR = GREY
TEXT_COLOR = BLACK
BORDER_COLOR = BRIGHT_BLUE
BASIC_FONT_SIZE = 22

MESSAGE_COLOR = WHITE

# Set margin.
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

board = [[0,0,1,2,2,3],
        [0,0,1,0,0,3],
        [0,0,1,9,9,3],
        [0,0,0,5,4,4],
        [8,7,7,5,0,0],
        [8,0,0,5,6,6]]

result = [(1, 1), (2, -1), (2, -1), (6, -1), (6, -1), (7, -1), (1, 1), (1, 1), (99, -1), (99, -1), (4, -1), (8, -1), (4, -1), (4, -1), (5, -1), (6, -1), (6, -1), (99, -1), (1, -1), (1, -1), (7, 1), (7, 1), (7, 1), (1, 1), (1, 1), (99, 1), (6, 1), (2, -1), (6, 1), (6, 1), (99, -1), (1, -1), (8, -1), (8, -1), (1, -1), (1, -1), (5, -1), (5, -1), (4, 1), (6, 1), (5, -1), (1, 1), (2, 1), (2, 1), (2, 1), (1, -1), (5, 1), (6, -1), (8, -1), (3, 1), (2, 1), (4, -1), (5, 1), (5, 1), (1, 1), (1, 1), (1, 1), (99, 1), (6, -1), (6, -1), (6, -1), (99, -1), (1, -1), (1, -1), (7, -1), (7, -1), (7, -1), (1, -1), (5, -1), (5, -1), (5, -1), (1, 1), (1, 1), (1, 1), (99, 1), (4, 1), (4, 1), (4, 1), (99, 1), (99, 1), (3, 1), (3, 1), (99, 1)]

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_RECT, NEW_RECT, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)

    mainBoard, solutionSeq = generate_new_puzzle(80)

    # Main game loop.
    while True:
        # The direction, if any, a tile should slide.
        slideTo = None
        draw_board(mainBoard)

        check_for_quit()

        if slideTo:
            # Show slide on screen.
            slide_animation(mainBoard, slideTo, 8)
            make_move(mainBoard, slideTo)
            # Record the slide.
            #allMoves.append(slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def get_left_top_tile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def draw_tile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = get_left_top_tile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILE_COLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXT_COLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def make_text(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def draw_board(board):
    DISPLAYSURF.fill(BACKGROUND_COLOR)


    for tiley in range(len(board)):
        for tilex in range(len(board[0])):
            if board[tilex][tiley]:
                draw_tile(tiley, tilex, board[tilex][tiley])

    left, top = get_left_top_tile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDER_COLOR, (left - 5, top - 5, width + 11, height + 11), 4)


# def make_move(board, move):
#     # This function does not check if the move is valid.
#     blankx, blanky = getBlankPosition(board)
#
#     if move == UP:
#         board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
#     elif move == DOWN:
#         board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
#     elif move == LEFT:
#         board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
#     elif move == RIGHT:
#         board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
#

def slide_animation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.


    # blankx, blanky = getBlankPosition(board)
    # if direction == UP:
    #     movex = blankx
    #     movey = blanky + 1
    # elif direction == DOWN:
    #     movex = blankx
    #     movey = blanky - 1
    # elif direction == LEFT:
    #     movex = blankx + 1
    #     movey = blanky
    # elif direction == RIGHT:
    #     movex = blankx - 1
    #     movey = blanky

    # prepare the base surface
    draw_board(board)
    baseSurf = DISPLAYSURF.copy()

def generate_new_puzzle(result):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []

    draw_board(board)
    pygame.display.update()
    pygame.time.wait(500)  # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = result
        slide_animation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
        make_move(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)



if __name__ == '__main__':
    main()