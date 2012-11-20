#!/usr/bin/env python

from time import sleep
from random import randint
import pygame

import conf
import core
import interesting

def main():

    pygame.init()
    screen = pygame.display.set_mode((conf.win_width, conf.win_height))
    screen.fill( conf.clear_color )

    # start game engine related stuff (yeah right)
    manager = core.SceneManager()
    scene = interesting.MainMenu(manager)
#    scene = interesting.Game(manager)
    keyboard_controller = interesting.MenuKeyboardController(scene) # FIXME: Move this controller inside the scene or something
    manager.append(scene)

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
                        else:
                            keyboard_controller.control(e.key)

            # update stuff
            manager.update(0.1) # TODO: 0.1 is temp for `dt`

            if run:
                screen.fill( conf.clear_color )

                # draw stuff
                manager.render(screen)

                pygame.display.flip()
                sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        print "OK bye."

if __name__ == "__main__":
    main()
