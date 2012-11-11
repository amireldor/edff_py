import pygame
from random import randint

import conf
import core
import interesting

class MainMenu(core.Scene):
    def __init__(self):
        core.Scene.__init__(self)

        self.models = [
            MenuItem("start"),
            MenuItem("options"),
            MenuItem("sing a song along"),
            MenuItem("exit")
        ]
        self.models[0].selected = True

        item_view = MenuItemView()
        item_view.models += self.models

        self.views.append(item_view)

class MenuItem(core.Model):
    def __init__(self, title):
        core.Model.__init__(self)
        self.title = title
        self.selected = False

class MenuItemView(core.View):
    def __init__(self):
        core.View.__init__(self)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.color = (0, 127, 255)
        self.selected_color = (255, 127, 255)

    def render(self, screen):
        y = 20
        for m in self.models:

            if m.selected:
                color = self.selected_color
            else:
                color = self.color

            text = self.font.render(m.title, True, color)
            screen.blit(text, (100, y))

            y += 16

class MenuKeyboardController(object): # TODO: inherit from a currently-non-existing core.Controller?
    def __init__(self):
        self.menu_models = None

    def associate_with(self, menu_models):
        self.menu_models = menu_models

    def control(self, controller_input):

        # handle up/down arrows
        if controller_input in (pygame.K_DOWN, pygame.K_UP):

            # `offset_index` is how much to move towards the next menu item
            if (controller_input == pygame.K_UP):
                direction = 'up'
                offset_index = -1
            else:
                direction = 'down'
                offset_index = +1

            # search which item is selected and make the next menu item selected instead of it
            for index in xrange(len(self.menu_models)):

                if self.menu_models[index].selected == True:
                    self.menu_models[index].selected = False

                    next_index = index + offset_index

                    if direction == 'up' and index == 0:
                        next_index = len(self.menu_models)-1

                    if direction == 'down' and index >= len(self.menu_models)-1:
                        next_index = 0

                    self.menu_models[next_index].selected = True
                    break

class Game(core.Scene):
    def __init__(self):
        core.Scene.__init__(self)

        # Stuff to show in the scene
        # - adding views
        enemy_view = interesting.EnemyView()
        matos_view = interesting.MatosView()
        self.views.append(matos_view)
        self.views.append(enemy_view)

        # - creating matos
        matos = interesting.Matos()
        self.models.append(matos)
        matos_view.models.append(matos)

        # - enemies
        for x in xrange(5):
            enemy = interesting.Enemy(matos)
            self.models.append(enemy)
            enemy_view.models.append(enemy)


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
