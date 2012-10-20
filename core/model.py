class Model(object):

    KEEP = 0
    REMOVE = 1

    def __init__(self):
        self.status = Model.KEEP

    def update(self, dt):
        pass


class Actor(Model):

    def __init__(self):
        Model.__init__(self)

        self.x = 0
        self.y = 0
        self.ix = 0
        self.iy = 0
