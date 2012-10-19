#!/usr/bin/env python

from time import sleep

class Model(object):

    REMOVE = 1

    def update(self, dt):
        pass


class Music(Model):
    
    def __init__(self):
        Model.__init__(self)

    def update(self, dt):
        print 'papam!'


class Scene(Model):

    def __init__(self):
        Model.__init__(self)
        self.models = []

    def update(self, dt):
        for x in self.models:
            x.update()


class MainMenu(Scene):

    def __init__(self):
        Scene.__init__(self)

    def update(self, dt):
        Scene.update(self, dt)
        print "Choose", range(1, 4)

        return [Model.REMOVE, Game()]


class Game(Scene):

    def __init__(self):
        Scene.__init__(self)

    def update(self, dt):
        Scene.update(self, dt)
        print "Lousy Man"


def main():
    current_scene = MainMenu()

    root = []
    root += [ Music(), current_scene ]

    try:
        while True:

            # make a copy of `root` because I feel bad mutating a list while iterating upon it
            new_root = root

            # iterate on `root`
            for x in root:
                ret = x.update(1)

                # do entity want to die?
                if ret and ret[0] == Model.REMOVE:
                    new_root.remove(x)

                    # if entity left something interesting, add it
                    if ret[1]:
                        new_root.append(ret[1]) 

            root = new_root

            sleep(1)

    except KeyboardInterrupt:
        print "OK bye."


if __name__ == "__main__":
    main()
