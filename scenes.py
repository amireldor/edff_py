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
        self.arm = models.Arm(self)
        arm_view.models.append(self.arm)

        # setup some fruit
        self.fruit = []
        self.fruit_view = views.FruitView(conf.images + "fruit.png", conf.fruit.dimensions)

        # setup scene
        self.new_fruit(self.arm)
        self.views += [monkey_view, arm_view, self.fruit_view]
        self.models += [self.monkey, self.arm]

    def new_fruit(self, arm):
        """Adds new fruit to the scene"""
        new_fruit = models.Fruit(arm)
        self.fruit.append(new_fruit)
        arm.set_fruit(new_fruit)

        self.models.append(new_fruit)
        self.fruit_view.models.append(new_fruit)

    def on_event(self, event):
        core.Scene.on_event(self, event)

        if event.type is pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            self.monkey.target_x = mouse_x
