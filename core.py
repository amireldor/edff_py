class Model(object):
    def __init__(self):
        self.keep = True

    def die(self):
        self.keep = False

    def should_remove(self):
        return not self.keep

    def update(self, dt):
        pass

class View(object):
    def __init__(self):
        self.models = []

    def render(self, screen):
        pass

class Scene(object):
    def __init__(self):
        self.models = []
        self.views = []

    def update(self, dt):
        for model in self.models:
            model.update(dt)

        self.models[:] = [ m for m in self.models if not m.should_remove() ]

    def render(self, screen):
        for view in self.views:
            view.render(screen)
            # FIXME: how to remove an unneeded view?
