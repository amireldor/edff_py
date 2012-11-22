import math

def restrict_0_360(angle):
    """ If you pass it 370, it will return 10. If you pass it -10 it will return 350 """

    rounds = math.floor(angle / 360.0)
    angle -= 360 * rounds

    return angle
