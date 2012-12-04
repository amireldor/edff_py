import pygame
from random import randint

import conf
import core

import models
import views

import imagegenerator

class Game(core.Scene):
    def __init__(self, manager):
        core.Scene.__init__(self, manager)

        # setup monkey
        #monkey_view = views.MonkeyView(conf.images + "monkey.png", conf.monkey.dimensions)
        monkey_view = views.MonkeyView([conf.images + "monkey.png", conf.images + "monkey_closed.png"], conf.monkey.dimensions)
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

        # create background image (clouds and such)
        self.background = pygame.Surface((conf.win_width, conf.win_height))
        self.background.fill(conf.clear_color)

        for x in xrange(3):
            image = imagegenerator.cloud()

            min_w, max_w = -conf.cloud.max_width/2, conf.win_width + conf.cloud.max_width/2
            min_h, max_h = -conf.cloud.max_height/2, (conf.win_height / 2) - conf.cloud.max_height/2

            self.background.blit( image, (randint(min_w, max_w), randint(min_h, max_h)) )


    def new_fruit(self, arm):
        """Adds new fruit to the scene"""
        new_fruit = models.Fruit(arm, self.monkey)
        self.fruit.append(new_fruit)
        arm.set_fruit(new_fruit)

        self.models.append(new_fruit)
        self.fruit_view.models.append(new_fruit)

    def on_event(self, event):
        core.Scene.on_event(self, event)
        # putting all control here is a bit ugly, I should make some
        # sort of Controllers like I once tried in 'core' or
        # something.

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            self.monkey.target_x = mouse_x

        elif event.type == pygame.MOUSEBUTTONDOWN and not self.monkey.is_closed():
            self.monkey.close_mouth()

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        core.Scene.render(self, screen)
