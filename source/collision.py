import pygame
import math

radius = 25
COS_30 = math.cos(math.radians(30))
SIN_30 = math.sin(math.radians(30))
rCOS_30 = radius * COS_30
rSIN_30 = radius * SIN_30


def render_collision_hex(surface, x, y, color):
    """ Draws the given hexagon. """

    render_collision_hex_raw(surface, 50 + x * (2 * rCOS_30) +
                            (11 - y) * (rCOS_30),
                            110 + y * (3 * rSIN_30),
                            color)

def render_collision_hex_raw(surface, x, y, color):
    """ Draws a hexagon at the given coordinates. """

    vertices = [
        (x, y + radius),
        (x + (rCOS_30), y + (rSIN_30)),
        (x + (rCOS_30), y - (rSIN_30)),
        (x, y - radius),
        (x - (rCOS_30), y - (rSIN_30)),
        (x - (rCOS_30), y + (rSIN_30))
    ]

    pygame.draw.polygon(surface, color, vertices)

def generate_collision_grid():
    """
    Renders to a temporary surface in order to get
    mouse coordinate-tile mappings.
    """

    # create the empty surface and data set
    temp = pygame.Surface((800, 600))
    data = [[() for x in xrange(800)] for y in xrange(600)]

    # render reference surface
    # we are encoding the (x, y) in the (r, g) coords
    temp.fill((128,128,128))
    for x in xrange(11):
        for y in xrange(11):
            render_collision_hex(temp, x, y, (x, y, 0))

    # create data set by looking at each pixel and decoding
    for x in xrange(800):
        for y in xrange(600):
            r, g, b, a = temp.get_at((x, y))
            if b:
                data[y][x] = None
            else:
                data[y][x] = (r, g)

    return data
            

