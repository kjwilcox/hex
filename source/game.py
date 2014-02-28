
import grid

import pygame
from pygame.locals import *

import math

radius = 25
COS_30 = math.cos(math.radians(30))
SIN_30 = math.sin(math.radians(30))
rCOS_30 = radius * COS_30
rSIN_30 = radius * SIN_30

class Game():
    """ A generic class with common functions for all games. """

    # some trig constants
    radius = 25
    COS_30 = math.cos(math.radians(30))
    SIN_30 = math.sin(math.radians(30))
    rCOS_30 = radius * COS_30
    rSIN_30 = radius * SIN_30
    
    def __init__(self, menu_data):
        """
        Initializes a general game class.
        Takes a dict containing some important data.
        """

        # I like to picture this making an
        # OM NOM NOM NOM sound as it steals the resources
        # from the menu.
        self.images = menu_data["images"]
        self.sounds = menu_data["sounds"]
        self.font = menu_data["font"]
        self.collision = menu_data["collision"]

        self.screen = menu_data["screen"]

        self.data = grid.Grid(11)

        self.hover = None
        self.mouse = None

    def __del__(self):
        """ Sets the title back to "Hex" after the game is done. """
        pygame.display.set_caption("Hex")

    def render(self):
        """ Generalized function for rendering, should be overwritten. """

        self.render_grid()
        pygame.display.flip()

    def render_grid(self):
        """ Renders the screen. """
        for x in range(self.data.size):
            for y in range(self.data.size):
                color = (245, 245, 245)
                if self.data.get(x, y) is 1:
                    color = (200, 0, 0)
                elif self.data.get(x, y) is 2:
                    color = (0, 0, 200)
                else:
                    if (x, y) == self.hover:
                        if self.player is 1:
                            color = (255, 100, 100)
                        else: # self.player is 2:
                            color = (100, 100, 255)
                    else:
                        color = (245, 245, 245)
                self.render_hex(x, y, color)
   
        
    def render_hex(self, x, y, color):
        """ Draws the given hexagon. """

        self.render_hex_raw(50 + x * (2 * rCOS_30) + (11 - y) * (rCOS_30),
                            110 + y * (3 * rSIN_30),
                            color)

    def render_hex_raw(self, x, y, color):
        """ Draws a hexagon at the given coordinates. """

        vertices = [
            (x, y + radius),
            (x + rCOS_30, y + rSIN_30),
            (x + rCOS_30, y - rSIN_30),
            (x, y - radius),
            (x - rCOS_30, y - rSIN_30),
            (x - rCOS_30, y + rSIN_30)
        ]

        pygame.draw.polygon(self.screen, color, vertices)
        pygame.draw.polygon(self.screen, (0,0,0), vertices, 3)
        #pygame.draw.aalines(self.screen, (0,0,0), True, vertices, 3)

    def update_mouse(self):
        """ Figures out which cell the mouse is over. """
        x, y = pygame.mouse.get_pos()
        if self.collision[y][x]:
            self.hover = self.collision[y][x]
        else:
            self.hover = None

    def switch_players(self):
        """ 1 -> 2, 2 -> 1 """
        if self.player is 1:
            self.player = 2
        else:
            self.player = 1

    def get_victory(self):
        """ Returns victory status. """
        if self.data.is_chain('h', 1):
            return 1
        elif self.data.is_chain('v', 2):
            return 2
        else:
            return 
