import pygame, random, sys
from pygame.locals import *
from collections import Counter


class Visualisation:
    def __init__(self, root, solution, tile=80):
        self.vehicles = list(root.vehicles)
        self.solution = solution
        self.tile = tile
        self.width = (root.width + 1) * self.tile
        self.colors = self.get_colors(root.board)

        # initialize pygame and window
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption('Rush Hour')
        self.window.fill((255, 255, 255))
        self.draw_board()
        pygame.display.update()

        # pause visualisation (wait for input)
        self.pause()

        # start visualisation
        self.run()

    def check_input(self):
        """
        checks for input which pauses or quits the visualisation
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit()
                self.pause()

    @staticmethod
    def get_colors(board):
        """
        creates random colors for each vehicle (except for the main vehicle)
        :param board: board representation from root node
        :return: dictionary containing colors
        """

        array = list()
        for row in board:
            array.extend(row)

        # create dictionary with a color for each index found in the board
        indexes = Counter(array)
        indexes.pop(None)
        for index in indexes:
            indexes[index] = (130 + int(random.random() * 60), int(random.random() * 256), int(random.random() * 256))

        # recolor the main vehicle
        indexes[0] = (255, 0, 0)

        return indexes

    @staticmethod
    def exit():
        """
        quit the visualisation
        """
        pygame.quit()
        sys.exit()

    def pause(self):
        """
        pause the visualisation, wait for input
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()
                    return False

    def run(self):
        """
        start the visualisation, which will pause after completing
        """

        # iterate over the moves in the solution
        while len(self.solution) > 0:
            self.check_input()
            self.window.fill((255, 255, 255))
            self.update_vehicles(self.solution.pop(0))
            self.draw_board()
            pygame.display.update()
            pygame.time.wait(150)

        # wait for input to quit
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN:
                    self.exit()

    def update_vehicles(self, step):
        index = step[0]
        move = step[1]

        # move the vehicle
        vehicle = self.vehicles[index]
        self.vehicles[index] = (vehicle[0], vehicle[1], vehicle[2] + move, vehicle[3] + move)

    def draw_board(self):
        """
        draw the current vehicles on the window
        """
        for index, vehicle in enumerate(self.vehicles):
            length = (vehicle[3] - vehicle[2]) + 1

            # draw horizontally orientated vehicles
            if vehicle[0]:
                pygame.draw.rect(self.window, self.colors[index], (vehicle[2] * self.tile, vehicle[1] * self.tile,
                                                                   length * self.tile, self.tile))
            # draw vertically orientated vehicles
            else:
                pygame.draw.rect(self.window, self.colors[index], (vehicle[1] * self.tile, vehicle[2] * self.tile,
                                                                   self.tile, length * self.tile))
