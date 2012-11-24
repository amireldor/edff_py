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

    def set_fruit(self, fruit):
        self.fruit = fruit
        self.fruit.in_hand(self)

    def get_fruit(self):
        return self.fruit

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

            if self.rotation <= conf.arm.throw_angle and not self.fruit.is_flying():
                self.fruit.fly( (-10, 0) )

class Fruit(core.Model):

    IN_HAND = 1
    FLYING = 2

    def __init__(self, arm):
        core.Model.__init__(self)
        self.x, self.y  = 0, 0
        self.rotation = 360 * random()
        self.rot_inc = -conf.fruit.rot_inc_max + (random() * conf.fruit.rot_inc_max * 2)

        self.in_hand(arm)

    def in_hand(self, arm):
        """Fruit will follow arm's hand position"""
        self.stage = Fruit.IN_HAND
        self.arm = arm

    def fly(self, speed):
        """Fruit will fly according to `speed` which is supposed to be a tuple
        with (inc_x, inc_y)"""
        self.stage = Fruit.FLYING
        self.speed = speed

    def is_flying(self):
        if self.stage == Fruit.FLYING:
            return True

        return False

    def update(self, dt):
        core.Model.update(self, dt)
        self.rotation += self.rot_inc * dt

        if self.stage == Fruit.IN_HAND:
            # put the fruit inside the arm's palm
            x, y = self.arm.x, self.arm.y
            x, y = util.forward( (x, y), conf.arm.dimensions[0], self.arm.rotation) # to the edge of arm
            x, y = util.forward( (x, y), conf.arm.fruit_tweak.ammount, self.arm.rotation + conf.arm.fruit_tweak.direction) # move a bit in the tweaking's direction
            self.x, self.y  = x, y
        elif self.stage == Fruit.FLYING:
            pass
