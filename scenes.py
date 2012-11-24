import pygame
from random import randint

import conf
import core

import models
import views

class Game(core.Scene):
    def __init__(self, manager):
        core.Scene.__init__(self, manager)

        # setup monkey
        monkey_view = views.MonkeyView(conf.images + "monkey.png", conf.monkey.dimensions)
        self.monkey = models.Monkey()
        monkey_view.models.append(self.monkey)

        # setup arm
        arm_view = views.ArmView(conf.images + "arm.png", conf.arm.dimensions)
        self.arm = models.Arm()
        arm_view.models.append(self.arm)

        # setup scene
        self.views += [monkey_view, arm_view]
        self.models += [self.monkey, self.arm]

        # temp tests
        fruit_view = views.FruitView(conf.images + "fruit.png", conf.fruit.dimensions)
        self.fruit = [ models.Fruit(self.arm), models.Fruit(self.arm), models.Fruit(self.arm) ]
        self.models += self.fruit
        fruit_view.models += self.fruit
        self.views += [fruit_view]

    def on_event(self, event):
        core.Scene.on_event(self, event)

        if event.type is pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            self.monkey.target_x = mouse_x
            self.arm.x = mouse_x
            self.arm.y = mouse_y
