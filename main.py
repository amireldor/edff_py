#!/usr/bin/env python

from time import sleep
from random import randint
import pygame

from core.model import Model
from core.scene import Scene
from interesting.scenes import MainMenu, Game
import conf

class Music(Scene):
    
    def __init__(self):
        pass

    def update(self, dt):
        self.track = randint(1, 10)

    def render(self, screen):
        print 'papam!', self.track

def main():

    pygame.init()
    screen = pygame.display.set_mode((conf.win_width, conf.win_height))
    screen.fill( conf.clear_color )

    root = []
    root += [ Music(), Game() ]

    try:
        run = True

        while run:

            # process events
            if pygame.event.peek():
                events = pygame.event.get()

                for e in events:

                    # quit event
                    if e.type == pygame.QUIT:
                        run = False

                    # quit on escape
                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            run = False


            if run:
                # make a copy of `root` because I feel bad mutating a list while iterating upon it
                new_root = root

                # iterate on `root` and update
                for x in root:
                    ret = x.update(1)

                    # do entity want to die?
                    if ret and ret[0] == Scene.REMOVE:
                        new_root.remove(x)

                        # if entity left something interesting, add it
                        if ret[1]:
                            new_root.append(ret[1])

                root = new_root

                # iterate on `root` and render
                screen.fill( conf.clear_color )
                for x in root:
                    x.render(screen)

                pygame.display.flip()
                sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        print "OK bye."

if __name__ == "__main__":
    main()
