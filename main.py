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

    game = scenes.Game(manager)
    pause = scenes.Pause(manager)
    intro = scenes.Intro(manager)

    game.set_pause_scene(pause)
    pause.set_game_scene(game)
    pause.activate(False)

    manager.append(intro)
    manager.append([game, pause])

    clock = pygame.time.Clock();

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
                dt = clock.get_fps();
                if not dt:
                    dt = 0.001
                else:
                    dt = 1.0 / dt
                manager.update(dt)

                # draw stuff
                screen.fill(conf.clear_color)
                manager.render(screen)

                pygame.display.flip()

            clock.tick()

    except KeyboardInterrupt:
        pass

    finally:
        print "OK bye."

if __name__ == "__main__":
    main()
