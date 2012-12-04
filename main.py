#!/usr/bin/env python

from time import sleep
import pygame

import conf
import core
import scenes

def main():
    pygame.init()
    screen = pygame.display.set_mode((conf.win_width, conf.win_height))

    # start game engine related stuff (yeah right)
    manager = core.SceneManager()
    scene = scenes.Game(manager)
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

                    manager.on_event(e)

            if run:
                # update stuff
                manager.update(0.01) # TODO: 0.1 is temp for `dt`

                # draw stuff
                manager.render(screen)

                pygame.display.flip()
                sleep(0.01)

    except KeyboardInterrupt:
        pass

    finally:
        print "OK bye."

if __name__ == "__main__":
    main()
