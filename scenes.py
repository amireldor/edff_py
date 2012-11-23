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
        monkey_view = views.MonkeyView()
        self.monkey = models.Monkey()
        monkey_view.models.append(self.monkey)

        # setup arm
        arm_view = views.ArmView()
        self.arm = models.Arm()
        arm_view.models.append(self.arm)

        # setup scene
        self.views += [monkey_view, arm_view]
        self.models += [self.monkey, self.arm]

        # temp tests
        fruit_view = views.FruitView()
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
