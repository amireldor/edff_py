import pygame
import math

import conf
import core
import util

import imagegenerator

class HasImageView(core.View):
    """Derive from me to have a nice image in you.

    Give me an image filename and
    a tuple of (width, height) to __init__.

    Alternatively, provide me with a list of filenames instead of a single
    filename and I'll load them all into a nice list (all with the same size of
    the tuple. Sorry).
    """

    def __init__(self, filename, dimensions):
        core.View.__init__(self)

        dimensions = int(dimensions[0] * conf.factor_width), int(dimensions[1] * conf.factor_height)

        # check if we got a list of filenames
        if isinstance(filename, type([])):
            # got a list, load each
            self.image = []
            for name in filename:
                self.image.append(pygame.image.load(name))
                self.image[-1] = pygame.transform.smoothscale(self.image[-1], dimensions)
        else:
            # got single filename, load it
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.smoothscale(self.image, dimensions)

class MonkeyView(HasImageView):
    """Give me Monkey()s and I'll draw them"""

    def __init__(self, filename, dimensions):
        HasImageView.__init__(self, filename, dimensions)
        rect = self.image[0].get_rect()

    def render(self, screen):
        HasImageView.render(self, screen)
        for model in self.models:
            x, y = model.x, model.y
            img_index = 0
            if model.is_closed():
                img_index = 1

            # move x to 'hotpoint' which is the middle bottom of the monkey rect
            rect = self.image[img_index].get_rect()

            # from scene coordinates to window coordinates
            x = int(x * conf.factor_width)
            y = int(y * conf.factor_height)

            # from scene coordinates, bottom of scene, to window coordinates, with the hotpoint being (top, left) instead of (middle, bottom)
            x -= rect.center[0]
            y -= rect.height

            screen.blit(self.image[img_index], (x, y))

class ArmView(HasImageView):
    """Give me the Arm() and I'll draw it"""

    def __init__(self, filename, dimensions):
        HasImageView.__init__(self, filename, dimensions)

    def render(self, screen):
        HasImageView.render(self, screen)
        for model in self.models:
            x, y = model.x, model.y

            rotated_img = pygame.transform.rotate(self.image, model.rotation)

            rot_rect = rotated_img.get_rect().center
            x -= rot_rect[0]
            y -= rot_rect[1]

            # move (x, y) to the edge of the arm
            half = conf.arm.dimensions[0] / 2
            x, y = util.forward((x, y), half, model.rotation)

            screen.blit(rotated_img, (x, y))

class FruitView(HasImageView):
    """Give me a Fruit() and I'll draw it"""

    def __init__(self, filename, dimensions):
        HasImageView.__init__(self, filename, dimensions)

    def render(self, screen):
        HasImageView.render(self, screen)
        for model in self.models:
            x, y = model.x, model.y

            # image manipulations
            to_render = self.image
            new_size = (int(conf.fruit.dimensions[0]*model.size_factor), int(conf.fruit.dimensions[1]*model.size_factor))
            if new_size[0] > 1 and new_size[1] > 1:
                # FIXME: is there a bug here :(?
                to_render = pygame.transform.scale( to_render, new_size )
            else:
                continue
            to_render = pygame.transform.rotate(to_render, model.rotation)

            rot_rect = to_render.get_rect().center
            x -= rot_rect[0]
            y -= rot_rect[1]

            screen.blit(to_render, (x, y))

class CloudView(core.View):
    def __init__(self):
        core.View.__init__(self)

        self.images = [] # actual cloud images

    def append(self, what):
        self.images.append( imagegenerator.cloud() )
        core.View.append(self, what)

    def pop_image(self):
        self.images.pop(0)

    def render(self, screen):
        core.View.render(self, screen)
        index = 0
        for model in self.models:
            screen.blit( self.images[index], (model.x, model.y) )
            index += 1

class TreeView(HasImageView):
    def __init__(self, filename, size):
        HasImageView.__init__(self, filename, size)

    def render(self, screen):
        HasImageView.render(self, screen)

        for model in self.models:
            screen.blit(self.image, (model.x, model.y))

class RotoZoom(core.View):
    def __init__(self, image):
        core.View.__init__(self)
        self.image = image

    # TODO: check for duplicated code in arm and in fruit views
    def render(self, screen):
        core.View.render(self, screen)
        for model in self.models:
            x, y = model.x, model.y

            # image manipulations
            to_render = self.image
            size_rect = self.image.get_rect()
            to_render = pygame.transform.rotozoom(to_render, model.rotation, model.zoom)

            rot_rect = to_render.get_rect().center
            x -= rot_rect[0]
            y -= rot_rect[1]

            screen.blit(to_render, (x, y))
