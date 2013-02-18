"""This module generates different images to be used in Eat Da Fruit Fruit.

Images are clouds and trees and fences in the zoo."""

import pygame
from random import randint

import conf

def my_rand(a, b):
    if b > a:
        return randint(a, b)
    else:
        return randint(b, a)

def cloud(dimensions, radius_factor):
    """`dimensions` - a (max_width, max_height)"""

    max_width = dimensions[0]
    max_height = dimensions[1]

    surface = pygame.Surface((max_width, max_height * 2))
    surface.set_colorkey( (0, 0, 0) )

    white = (255, 255, 255)

    # TODO: min/max_circles should be an argument to this function and not conf
    for x in xrange(my_rand(conf.cloud.min_circles, conf.cloud.max_circles)):
        radius = my_rand(int(max_width * radius_factor), min(max_width, max_height) / 2)

        x = my_rand(radius, max_width-radius)
        y = my_rand(radius, max_height*2-radius)

        pygame.draw.circle( surface, white, (x, y), radius )

    rect = surface.get_rect()
    rect.height -= max_height

    surface = surface.subsurface( rect )

    return surface
