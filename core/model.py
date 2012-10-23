class Model(object):

    KEEP = 0
    REMOVE = 1

    def __init__(self):
        self.status = Model.KEEP # FIXME: I don't think `status` is the appropriate word

    def update(self, dt):
        pass

    def remove_me(self):
        """Asks the caller to `update` to remove me from the list in the next iteration"""
        self.status = Model.REMOVE

    def should_remove(self):
        return self.status == Model.REMOVE

    def keep_me(self):
        """ Revert a request to remove myself. Caller to `update` should not require this to be called.
            It should keep the object by default. """
        self.status = Model.KEEP


class Actor(Model):

    def __init__(self):
        Model.__init__(self)

        self.x = 0
        self.y = 0
        self.ix = 0
        self.iy = 0
