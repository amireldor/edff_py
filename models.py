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

    PREPARE = 1
    THROW = 2

    def __init__(self):
        core.Model.__init__(self)

        self.x = conf.win_width
        self.y = conf.win_height * conf.arm.position_factor
        self.rotation = util.restrict_0_360(conf.arm.top_angle)

        self.stage = Arm.PREPARE

    def update(self, dt):
        core.Model.update(self, dt)

        # move arm angle according to stage
        if self.stage == Arm.PREPARE:
            self.rotation += (conf.arm.bottom_angle - self.rotation) * dt * conf.arm.prepare_factor
            if abs(self.rotation - conf.arm.bottom_angle) <= conf.arm.rotation_error:
                self.stage = Arm.THROW
        elif self.stage == Arm.THROW:
            self.rotation += (conf.arm.top_angle - self.rotation) * dt * conf.arm.throw_factor
            if abs(self.rotation - conf.arm.top_angle) <= conf.arm.rotation_error:
                self.stage = Arm.PREPARE


class Fruit(core.Model):
    def __init__(self, arm):
        core.Model.__init__(self)
        self.arm = arm
        self.x, self.y  = 0, 0
        self.rotation = 360 * random()
        self.rot_inc = -conf.fruit.rot_inc_max + (random() * conf.fruit.rot_inc_max)

    def update(self, dt):
        core.Model.update(self, dt)
        self.rotation += self.rot_inc * dt

        # put the fruit inside the arm's palm
        x, y = self.arm.x, self.arm.y
        x, y = util.forward( (x, y), conf.arm.dimensions[0], self.arm.rotation) # to the edge of arm
        x, y = util.forward( (x, y), conf.arm.fruit_tweak.ammount, self.arm.rotation + conf.arm.fruit_tweak.direction) # move a bit in the tweaking's direction

        self.x, self.y  = x, y

        # if random() < 0.01: self.dont_keep() # this is stam a check, and it passed successfully
