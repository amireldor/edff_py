import pygame

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
