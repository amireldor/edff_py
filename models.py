from random import random

import conf
import core
import util

class Monkey(core.Model):
    """The fruit-eating monkey.

    .-----.
    |     |
    |     |
    |     |
    '--O--'

    "O" is the origin of the monkey coordinates, so the mouth is calculated as
    something like (self.y - self.height).
    """

    def __init__(self):
        core.Model.__init__(self)

        self.x = conf.win_width / 2
        self.y = conf.win_height
        self.target_x = self.x

    def update(self, dt):
        core.Model.update(self, dt)
        self.x = self.target_x

class Arm(core.Model):
    """The fruit-throwing hand.

    .------------.
    |            |
    O            |
    |            |
    '------------'

    "O" is the origin of the monkey coordinates, so the throwing-point is
    calculated as something like (self.x - self.width).
    """

    def __init__(self):
        core.Model.__init__(self)

        self.x = conf.win_width
        self.y = conf.win_height * conf.arm.factor
        self.rotation = util.restrict_0_360(0)

    def update(self, dt):
        core.Model.update(self, dt)
        self.rotation = util.restrict_0_360(self.rotation + 360*dt)

class Fruit(core.Model):
    def __init__(self, arm):
        core.Model.__init__(self)
        self.arm = arm
        self.x, self.y  = self.arm.x, self.arm.y
        self.rotation = 360 * random()
        self.rot_inc = -conf.fruit.rot_inc_max + (random() * conf.fruit.rot_inc_max)

    def update(self, dt):
        core.Model.update(self, dt)
        self.rotation += self.rot_inc * dt
        self.x, self.y  = self.arm.x, self.arm.y

        # if random() < 0.01: self.dont_keep() # this is stam a check, and it passed successfully
