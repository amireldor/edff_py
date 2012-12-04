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
        monkey_view.append(self.monkey)

        # setup arm
        arm_view = views.ArmView(conf.images + "arm.png", conf.arm.dimensions)
        self.arm = models.Arm(self)
        arm_view.append(self.arm)

        # setup some fruit
        self.fruit = []
        self.fruit_view = views.FruitView(conf.images + "fruit.png", conf.fruit.dimensions)

        # setup background (clouds and such)
        self.clouds = []
        self.cloud_view = views.CloudView()

        self.cloud_creation_x = conf.win_width
        while self.cloud_creation_x > -conf.cloud.max_width:
            self.cloud_creation_x -= randint( conf.cloud.delta[0], conf.cloud.delta[1] )
            self.new_cloud( self.cloud_creation_x )

        # setup scene
        self.new_fruit(self.arm)
        self.views += [self.cloud_view, monkey_view, arm_view, self.fruit_view]
        self.models += [self.monkey, self.arm]

    def update(self, dt):
        core.Scene.update(self, dt)

        # this is kinda hacky, but I don't care
        self.cloud_creation_x += conf.cloud.max_ix * dt
        if self.cloud_creation_x >= -conf.cloud.max_width:
            self.new_cloud()
            self.cloud_creation_x -= randint( conf.cloud.delta[0], conf.cloud.delta[1] )

    def new_cloud(self, x=-conf.cloud.max_width):
            cloud = models.Cloud( (x, randint(-conf.cloud.max_height, conf.win_height/2 - conf.cloud.max_height)) , self.cloud_view )
            self.models.append(cloud)
            self.cloud_view.append(cloud)

    def new_fruit(self, arm):
        """Adds new fruit to the scene"""
        new_fruit = models.Fruit(arm, self.monkey)
        self.fruit.append(new_fruit)
        arm.set_fruit(new_fruit)

        self.models.append(new_fruit)
        self.fruit_view.append(new_fruit)

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
