import math


def distance_2d(startx, starty, targetx, targety):
    return math.sqrt(((startx-targetx)**2)+(starty-targety)**2)
