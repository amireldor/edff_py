class View(object):

    def __init__(self):
        self.actors = []

    def render_all(self, screen):
        for actor in self.actors:
            self.render(screen, actor)

    def render(self, screen, actor):
        pass
