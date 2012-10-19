class Model(object):

    REMOVE = 1

    def __init__(self):
        pass

    def update(self, dt):
        pass


class Actor(Model):

    def __init__(self):
        Model.__init__(self)

        self.x = 0
        self.y = 0
        self.ix = 0
        self.iy = 0
