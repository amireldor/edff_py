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

        tree_view = views.TreeView(conf.images + "tree.png", conf.tree.dimensions)
        for x in xrange(randint(1, conf.tree.max_trees)):
            pos = (randint(-conf.tree.dimensions[0], conf.win_width), randint(conf.win_height - conf.tree.dimensions[1], conf.win_height) )
            tree =  models.Tree(pos)
            self.models += [ tree ]
            tree_view.append(tree)

        # setup scene
        self.new_fruit(self.arm)
        self.views += [self.cloud_view, tree_view, monkey_view, arm_view, self.fruit_view]
        self.models += [self.monkey, self.arm]

        self.paused = False

    def pause(self, state=True):
        self.paused = state

    def update(self, dt):
        if self.paused:
            return

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

        elif event.type == pygame.KEYDOWN:
            #self.scene_manager.set_extra(PauseScene(self.scene_manager))
            pass

class Pause(core.Scene):
    def __init__(self, manager):
        core.Scene.__init__(self, manager)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        self.message = self.font.render("hello hit SPACEBAR to return", False, (0, 128, 255))

    def render(self, screen):
        rect = screen.get_rect()
        rect.x = 20
        rect.y = 20
        rect.width -= 40
        rect.height -= 40
        screen.fill( (255, 128, 0), rect )
        screen.blit( self.message, (40, 40) )

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #self.scene_manager.kill_extra()
            pass

class Blue(core.Scene):
    def __init__(self, manager):
        core.Scene.__init__(self, manager)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        self.message = self.font.render("hello hit RETURN to return", False, (255, 128, 255))

    def render(self, screen):
        rect = screen.get_rect()
        rect.x = 40
        rect.y = 40
        rect.width -= 80
        rect.height -= 80
        screen.fill( (0, 0, 255), rect )
        screen.blit( self.message, (60, 60) )

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            #self.scene_manager.kill_extra()
            pass
