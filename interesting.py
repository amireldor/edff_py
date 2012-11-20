import pygame
from random import randint

import conf
import core
import interesting

class MainMenu(core.Scene):
    def __init__(self, manager):
        core.Scene.__init__(self, manager)

        self.models = [
            MenuItem("start"),
            MenuItem("options"),
            MenuItem("sing a song along"),
            MenuItem("exit")
        ]
        self.models[0].selected = True
        self.menu_models = self.models # ref to the menu items, maybe later we'll have more models on this scene

        item_view = MenuItemView()
        item_view.models += self.models

        self.views.append(item_view)

    def on_event(self, event):
        core.Scene.on_event(self, event)

        if event.type is not pygame.KEYDOWN:
            return

        key = event.key

        # handle up/down arrows
        if key in (pygame.K_DOWN, pygame.K_UP):

            # `offset_index` is how much to move towards the next menu item
            if (key == pygame.K_UP):
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

        elif key == pygame.K_RETURN:
            self.scene_manager.append(Game(self.scene_manager))
            self.scene_manager.next()


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

class Game(core.Scene):

    HERO_STEP = 25
    ENEMY_STEP= 5

    def __init__(self, manager):
        core.Scene.__init__(self, manager)

        # Stuff to show in the scene
        # - adding views
        enemy_view = interesting.EnemyView()
        matos_view = interesting.MatosView()
        self.views.append(matos_view)
        self.views.append(enemy_view)

        # - creating matos
        self.matos = interesting.Matos()
        self.models.append(self.matos)
        matos_view.models.append(self.matos)

        # - enemies
        self.enemies = []
        for x in xrange(5):
            enemy = interesting.Enemy(self.matos)
            self.enemies.append(enemy)
            self.models.append(enemy)
            enemy_view.models.append(enemy)

    def on_event(self, event):
        core.Scene.on_event(self, event)

        if event.type is not pygame.KEYDOWN:
            return

        key = event.key

        # handle up/down arrows
        if key == pygame.K_LEFT:
            self.matos.x -= self.HERO_STEP
        elif key == pygame.K_RIGHT:
            self.matos.x += self.HERO_STEP
        elif key == pygame.K_UP:
            self.matos.y -= self.HERO_STEP
        elif key == pygame.K_DOWN:
            self.matos.y += self.HERO_STEP

    def update(self, dt):
        core.Scene.update(self, dt)

        self.enemies[:] = [ e for e in self.enemies if e.should_keep() ]

        # no enemies? back to main menu
        if not len(self.enemies):
            self.scene_manager.append(MainMenu(self.scene_manager))
            self.scene_manager.next()

class Matos(core.Model):
    def __init__(self):
        core.Model.__init__(self)

        self.x = randint(0, conf.win_width)
        self.y = randint(0, conf.win_height)
        self.radius = conf.matos.radius

    def update(self, dt):
        pass

class MatosView(core.View):
    def __init__(self):
        core.View.__init__(self)

    def render(self, screen):
        """Render self.model that someone has set for me."""
        self.models[:] = [ m for m in self.models if m.should_keep() ]

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
            self.dont_keep()

        else:
            self.x += randint(-Game.ENEMY_STEP, Game.ENEMY_STEP)
            self.y += randint(-Game.ENEMY_STEP, Game.ENEMY_STEP)

class EnemyView(core.View):
    def __init__(self):
        core.View.__init__(self)
        self.models = []

    def render(self, screen):
        """Render self.model that someone has set for me."""
        self.models[:] = [ m for m in self.models if m.should_keep() ]

        for model in self.models:
            pygame.draw.circle(screen, (0, 255, 127), (model.x, model.y), model.radius)

        return True
