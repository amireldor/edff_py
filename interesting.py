import pygame
from random import randint

import core
import conf

class Game(core.Scene):
    def __init__(self):
        core.Scene.__init__(self)

class Matos(core.Model):
    def __init__(self):
        core.Model.__init__(self)

        self.x = randint(0, conf.win_width)
        self.y = randint(0, conf.win_height)
        self.radius = conf.matos.radius

    def update(self, dt):
        self.x += randint(-25, 25)
        self.y += randint(-25, 25)

class MatosView(core.View):
    def __init__(self):
        core.View.__init__(self)
        self.models = []

    def render(self, screen):
        """Render self.model that someone has set for me."""
        self.models[:] = [ m for m in self.models if not m.should_remove() ]

        for model in self.models:
            pygame.draw.circle(screen, (255, 0, 0), (model.x, model.y), model.radius)

        return True

class Enemy(core.Model):
    def __init__(self, hero_matos):
        core.Model.__init__(self)

        self.x = randint(0, conf.win_width)
        self.y = randint(0, conf.win_height)
        self.radius = conf.matos.radius / 2

        self.hero_matos = hero_matos

    def update(self, dt):
        dist_square = (self.x - self.hero_matos.x)**2 + (self.y - self.hero_matos.y)**2
        if dist_square < (self.radius + self.hero_matos.radius)**2:
            self.die()

        else:
            self.x += randint(-5, 5)
            self.y += randint(-5, 5)

class EnemyView(core.View):
    def __init__(self):
        core.View.__init__(self)
        self.models = []

    def render(self, screen):
        """Render self.model that someone has set for me."""
        self.models[:] = [ m for m in self.models if not m.should_remove() ]

        for model in self.models:
            pygame.draw.circle(screen, (0, 255, 127), (model.x, model.y), model.radius)

        return True
