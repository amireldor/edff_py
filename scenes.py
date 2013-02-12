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
            pos = (randint(-conf.tree.dimensions[0]/2, conf.win_width-conf.tree.dimensions[0]/2), randint(conf.win_height-conf.tree.dimensions[1], conf.win_height-conf.tree.dimensions[1]/2) )
            tree =  models.Tree(pos)
            self.models += [ tree ]
            tree_view.append(tree)

        # rotating messages
        yousuck_font = pygame.font.SysFont(pygame.font.get_default_font(), conf.yousuck.size) # TODO: change default font
        self.yousuck_image = yousuck_font.render("you suck!", False, conf.yousuck.color)
        self.yousuck_view = views.RotoZoom(self.yousuck_image)

        # setup scene
        self.new_fruit(self.arm)
        #self.views += [self.cloud_view, tree_view, monkey_view, arm_view, self.fruit_view, self.yousuck_view]
        self.views = [self.cloud_view, tree_view, monkey_view] # TODO: this is temp
        self.models += [self.monkey, self.arm]

        self.pause_scene = None # the 'pause' scene

    def set_pause_scene(self, pause_scene):
        self.pause_scene = pause_scene

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
        new_fruit = models.Fruit(self)
        self.fruit.append(new_fruit)
        arm.set_fruit(new_fruit)

        self.models.append(new_fruit)
        self.fruit_view.append(new_fruit)

    def create_yousuck(self):
        img_rect = self.yousuck_image.get_rect()
        model = models.CoolZoom((randint(img_rect.width/2, conf.win_width - img_rect.width/2), randint(img_rect.height/2, conf.win_height - img_rect.height/2)))
        self.yousuck_view.append(model)
        self.models.append(model)

    def on_event(self, event):
        core.Scene.on_event(self, event)
        # putting all control here is a bit ugly, I should make some
        # sort of Controllers like I once tried in 'core' or
        # something.

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            self.monkey.target_x = mouse_x / conf.factor_width # win coords to scene coords

        elif event.type == pygame.MOUSEBUTTONDOWN and not self.monkey.is_closed() and self.is_active():
            self.monkey.close_mouth()

        elif event.type == pygame.KEYDOWN:
            self.activate(False)
            self.pause_scene.activate(True)

class Pause(core.Scene):
    def __init__(self, manager):
        """game is the game scene that should be (un)paused"""
        # TODO: change stuff to conf stuff
        core.Scene.__init__(self, manager)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 50) # TODO: change default font
        self.message = self.font.render("hello hit SPACEBAR to return", False, (0, 128, 255))
        self.game = None

    def set_game_scene(self, game):
        self.game = game

    def render(self, screen):
        core.Scene.render(self, screen)

        if not self.is_active():
            return

        screen.blit( self.message, (40, 40) )

    def on_event(self, event):
        core.Scene.on_event(self, event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.activate(False)
            self.game.activate(True)

class Intro(core.Scene):
    def __init__(self, manager):
        core.Scene.__init__(self, manager)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        self.image = pygame.image.load(conf.images + "baboonzoo_splash.png")
        self.image = pygame.transform.smoothscale(self.image, (conf.win_width, conf.win_height))

    def render(self, screen):
        screen.blit( self.image, (0, 0) )

    def on_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.get_manager().next()
