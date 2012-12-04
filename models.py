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

    OPENED = 0
    CLOSED = 1

    def __init__(self):
        core.Model.__init__(self)

        self.x = conf.win_width / 2
        self.y = conf.win_height
        self.target_x = self.x

        self.state = Monkey.OPENED
        self.mouth_timeout = conf.monkey.mouth_timeout

    def update(self, dt):
        core.Model.update(self, dt)
        self.x = self.target_x

        if self.is_closed():
            self.mouth_timeout -= 1000 * dt
            if self.mouth_timeout <= 0:
                self.mouth_timeout = conf.monkey.mouth_timeout
                self.open_mouth()

    def is_closed(self):
        """Is my mouth closed?"""
        return self.state == Monkey.CLOSED

    def close_mouth(self):
        self.state = Monkey.CLOSED

    def open_mouth(self):
        self.state = Monkey.OPENED

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

    def __init__(self, game):
        core.Model.__init__(self)
        self.game = game

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
                self.game.new_fruit(self)

            if self.stage == Arm.THROW and self.rotation <= conf.arm.throw_angle and not self.fruit.is_flying():
                self.fruit.fly( (conf.fruit.min_inc_x + random() * (conf.fruit.max_inc_x - conf.fruit.min_inc_x), random() * conf.fruit.max_init_inc_y) )

class Fruit(core.Model):

    IN_HAND = 1
    FLYING = 2
    EATEN = 3

    def __init__(self, arm, monkey):
        core.Model.__init__(self)
        self.x, self.y  = 0, 0
        self.rotation = 360 * random()
        self.rot_inc = -conf.fruit.rot_inc_max + (random() * conf.fruit.rot_inc_max * 2)

        self.in_hand(arm)
        self.monkey = monkey

        self.size_factor = 1

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
            self.x += self.speed[0] * dt
            self.y += self.speed[1] * dt
            self.speed = (self.speed[0], self.speed[1] + conf.gravity * dt)

            # check if out of screen
            if self.x < -conf.fruit.dimensions[0]/2 or self.y > conf.win_height + conf.fruit.dimensions[1]/2:
                self.dont_keep()

            # check if should be eaten
            if self.monkey.state == Monkey.CLOSED:
                x, y = util.forward( (self.monkey.x, self.monkey.y - conf.monkey.dimensions[1]), conf.monkey.mouth_tweak.ammount, conf.monkey.mouth_tweak.direction )
                dist = (self.x - x)**2 + (self.y - y)**2

                if dist <= conf.collision.fruit_monkey:
                    self.stage = Fruit.EATEN
                    self.rot_inc *= conf.fruit.rot_inc_extra

        elif self.stage == Fruit.EATEN:
            self.size_factor -= conf.fruit.shrink * dt
            if self.size_factor <= 0:
                self.size_factor = 0
                self.dont_keep()
