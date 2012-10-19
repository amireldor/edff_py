#!/usr/bin/env python

from time import sleep

from core.model import Model
from interesting.scenes import MainMenu, Game

class Music(Model):
    
    def __init__(self):
        Model.__init__(self)

    def update(self, dt):
        print 'papam!'

def main():
    root = []
    root += [ Music(), MainMenu() ]

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
