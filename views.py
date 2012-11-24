import pygame
import math

import conf
import core

class HasImageView(core.View):
    """Derive from me to have a nice image in you. Specify image filename and
    a tuple of (width, height) to __init__"""

    def __init__(self, filename, dimensions):
        core.View.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, dimensions)

class MonkeyView(HasImageView):
    """Give me Monkey()s and I'll draw them"""

    def __init__(self, filename, dimensions):
        HasImageView.__init__(self, filename, dimensions)

    def render(self, screen):
        core.View.render(self, screen)
        for model in self.models:
            screen.blit(self.image, (model.x - conf.monkey.dimensions[0] / 2, model.y - conf.monkey.dimensions[1]))

class ArmView(HasImageView):
    """Give me the Arm() and I'll draw it"""

    def __init__(self, filename, dimensions):
        HasImageView.__init__(self, filename, dimensions)

    def render(self, screen):
        core.View.render(self, screen)
        for model in self.models:
            x, y = model.x, model.y

            rotated_img = pygame.transform.rotate(self.image, model.rotation)

            rot_rect = rotated_img.get_rect().center
            x -= rot_rect[0]
            y -= rot_rect[1]

            half = conf.arm.dimensions[0] / 2
            x += half * math.cos(math.radians(model.rotation))
            y -= half * math.sin(math.radians(model.rotation))

            screen.blit(rotated_img, (x, y))

class FruitView(HasImageView):
    """Give me a Fruit() and I'll draw it"""

    def __init__(self, filename, dimensions):
        HasImageView.__init__(self, filename, dimensions)

    def render(self, screen):
        core.View.render(self, screen)
        for model in self.models:
            x, y = model.x, model.y

            rotated_img = pygame.transform.rotate(self.image, model.rotation)

            rot_rect = rotated_img.get_rect().center
            x -= rot_rect[0]
            y -= rot_rect[1]

            screen.blit(rotated_img, (x, y))
