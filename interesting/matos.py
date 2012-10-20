from core.model import Actor
import conf

class Matos(Actor):

    def __init__(self):
        Actor.__init__(self)

        self.x = 10 + conf.matos.radius
        self.y = conf.win_height / 2.0
        self.age = 0

    def update(self, dt):
        if (self.age < 20): # stam demonstration
            self.age += 1
        else:
            self.status = self.REMOVE
