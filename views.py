import pygame
import math

import conf
import core

class MonkeyView(core.View):
    """Give me Monkey()s and I'll draw them"""

    image = None

    def __init__(self):
        core.View.__init__(self)

        if not self.image:
            image = pygame.image.load(conf.images + 'monkey.png')
            image = pygame.transform.scale(image, (conf.monkey.width, conf.monkey.height))

            self.image = image

    def render(self, screen):
        for model in self.models:
            screen.blit(self.image, (model.x - conf.monkey.width / 2, model.y - conf.monkey.height))

class ArmView(core.View):
    """Give me the Arm() and I'll draw it"""

    image = None

    def __init__(self):
        core.View.__init__(self)

        if not self.image:
            image = pygame.image.load(conf.images + 'arm.png')
            image = pygame.transform.scale(image, (conf.arm.width, conf.arm.height))

            self.image = image

    def render(self, screen):
        for model in self.models:
            x, y = model.x, model.y

            rotated_img = pygame.transform.rotate(self.image, model.rotation)

            rot_rect = rotated_img.get_rect().center
            x -= rot_rect[0]
            y -= rot_rect[1]

            half = conf.arm.width / 2
            x += half * math.cos(math.radians(model.rotation))
            y -= half * math.sin(math.radians(model.rotation))

            screen.blit(rotated_img, (x, y))
