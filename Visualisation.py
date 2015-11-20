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
    SOLVEDBOARD = get_start_board()  # a solved board is the same as the board in a start state.
    # List of moves made from the solved configuration.
    allMoves = []

    # Main game loop.
    while True:
        # The direction, if any, a tile should slide.
        slideTo = None
        draw_board(mainBoard)

        check_for_quit()
        # Event handling loop.
        # for event in pygame.event.get():
        #     if event.type == MOUSEBUTTONUP:
        #         spotx, spoty = get_spot_clicked(mainBoard, event.pos[0], event.pos[1])
        #
        #         # Check if the clicked tile was next to the blank spot.
        #         if (blankx, blanky) == (get_black_position(mainBoard)):
        #             if spotx == blankx + 1 and spoty == blanky:
        #                 slideTo = LEFT
        #             elif spotx == blankx - 1 and spoty == blanky:
        #                 slideTo = RIGHT
        #             elif spotx == blankx and spoty == blanky + 1:
        #                 slideTo = UP
        #             elif spotx == blankx and spoty == blanky - 1:
        #                 slideTo = DOWN
        #

        if slideTo:
            # Show slide on screen.
            slide_animation(mainBoard, slideTo, 8)
            make_move(mainBoard, slideTo)
            # Record the slide.
            allMoves.append(slideTo)
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


def get_start_board():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = BLANK
    return board


def get_black_position(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def make_move(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = get_black_position(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def is_valid_move(board, move):
    blankx, blanky = get_black_position(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def get_random_move(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not is_valid_move(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not is_valid_move(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not is_valid_move(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not is_valid_move(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def get_left_top_tile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def get_spot_clicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = get_left_top_tile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


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

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                draw_tile(tilex, tiley, board[tilex][tiley])

    left, top = get_left_top_tile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDER_COLOR, (left - 5, top - 5, width + 11, height + 11), 4)


def slide_animation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = get_black_position(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    draw_board(board)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = get_left_top_tile(movex, movey)
    pygame.draw.rect(baseSurf, BACKGROUND_COLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        check_for_quit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            draw_tile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            draw_tile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            draw_tile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            draw_tile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_new_puzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = get_start_board()
    draw_board(board)
    pygame.display.update()
    pygame.time.wait(500)  # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = get_random_move(board, lastMove)
        slide_animation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
        make_move(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def reset_animation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:]  # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slide_animation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        make_move(board, oppositeMove)


if __name__ == '__main__':
    main()
