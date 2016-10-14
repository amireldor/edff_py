import pygame
from random import randint, random

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
        yousuck_font = pygame.font.Font(conf.fonts + "Prezident.ttf", conf.yousuck.size)
        self.yousuck_image = yousuck_font.render("YOU SUCK!", True, conf.yousuck.color)
        self.yousuck_view = views.RotoZoom(self.yousuck_image)

        # ---> you suck message
        msg_font = pygame.font.Font(conf.fonts + "Prezident.ttf", conf.message_size)
        # self.yousuck_image = yousuck_font.render("YOU SUCK!", True, conf.yousuck.color)

        # ---> pause message, TODO: move hardcoded values to conf
        pause_info = models.CoolZoom( (conf.scene_width / 2, conf.message_size), zoom_times=(0, 10), rotation_count=(0, 0.0016))
        pause_img = msg_font.render("HELLO, PRESSING ANY KEY WILL PAUSE.", True, (0, 0, 0))
        pause_view = views.RotoZoom(pause_img)
        pause_view.models = [pause_info]

        self.models += [pause_info]

        # setup scene
        self.new_fruit(self.arm)
        self.views += [self.cloud_view, tree_view, monkey_view, arm_view, self.fruit_view, self.yousuck_view, pause_view]
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

        count = conf.yousuck.rotation_count_range
        count = random() * (count[1] - count[0])
        random_rotation_count = (count, count * conf.yousuck.rotation_count_out_factor)

        model = models.CoolZoom((randint(img_rect.width/2, conf.scene_width - img_rect.width/2), randint(img_rect.height/2, conf.scene_height - img_rect.height/2)), rotation_count=random_rotation_count)

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

    background_image = None
    font = None
    message = None

    def __init__(self, manager):
        """game is the game scene that should be (un)paused"""
        # TODO: change stuff to conf stuff
        core.Scene.__init__(self, manager)

        if self.font == None:
            self.font = pygame.font.Font(conf.fonts + "Prezident.ttf", conf.pause.font_size )
        if self.message == None:
            self.message = self.font.render( "HELLO, HIT SPACEBAR TO CONTINUE.", True, conf.pause.font_color )

        if self.background_image == None:
            self.background_image = pygame.image.load(conf.images + conf.pause.background_image)
            self.background_image = pygame.transform.smoothscale(self.background_image, (conf.win_width, conf.win_height) )

        self.game = None

    def set_game_scene(self, game):
        self.game = game

    def render(self, screen):
        core.Scene.render(self, screen)

        if not self.is_active():
            return

        # background image
        screen.blit( self.background_image, (0, 0) )

        # pause message
        rect = self.message.get_rect()
        screen.blit( self.message, (conf.win_width / 2 - rect.width / 2, conf.win_height / 2 - rect.height / 2) )

    def on_event(self, event):
        core.Scene.on_event(self, event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.activate(False)
            self.game.activate(True)

class Intro(core.Scene):
    def __init__(self, manager):
        core.Scene.__init__(self, manager)
        self.font = pygame.font.Font(conf.fonts + "Prezident.ttf", 50)
        self.image = pygame.image.load(conf.images + "baboonzoo_splash.png")
        self.image = pygame.transform.smoothscale(self.image, (conf.win_width, conf.win_height))

    def render(self, screen):
        screen.blit( self.image, (0, 0) )

    def on_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.get_manager().next()
