class View(object):

    def __init__(self):
        self.actors = []

    def render_all(self, screen):
        self.remove_old()
        for actor in self.actors:
            self.render(screen, actor)

    def remove_old(self):
        """Iterate though actors that I should render and clean the dead ones"""
        new_actors = self.actors
        for actor in self.actors:
            if actor.status == actor.REMOVE:
                new_actors.remove(actor)
        self.actors = new_actors


    def render(self, screen, actor):
        pass
