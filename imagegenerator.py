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

def cloud():

    surface = pygame.Surface((conf.cloud.max_width, conf.cloud.max_height * 2))
    surface.set_colorkey( (0, 0, 0) )

    white = (255, 255, 255)

    for x in xrange(my_rand(conf.cloud.min_circles, conf.cloud.max_circles)):
        radius = my_rand(conf.cloud.min_radius, min(conf.cloud.max_width, conf.cloud.max_height) / 2)

        x = my_rand(radius, conf.cloud.max_width-radius)
        y = my_rand(radius, conf.cloud.max_height*2-radius)

        pygame.draw.circle( surface, white, (x, y), radius )

    rect = surface.get_rect()
    rect.height -= conf.cloud.max_height

    surface = surface.subsurface( rect )

    return surface
