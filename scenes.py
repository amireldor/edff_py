import pygame
from random import randint

import conf
import core

import models
import views

class Game(core.Scene):
    def __init__(self, manager):
        core.Scene.__init__(self, manager)

        monkey_view = views.MonkeyView()
        self.monkey = models.Monkey()
        monkey_view.models.append(self.monkey)

        self.views.append(monkey_view)
        self.models.append(self.monkey)

    def on_event(self, event):
        core.Scene.on_event(self, event)

        if event.type is pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            self.monkey.target_x = mouse_x
