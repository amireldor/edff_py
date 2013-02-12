import math

def restrict_0_360(angle):
    """ If you pass it 370, it will return 10. If you pass it -10 it will return 350 """

    rounds = math.floor(angle / 360.0)
    angle -= 360 * rounds

    return angle

def forward(coords, amount, angle):
    """Take the coords and make them move ammount of pixels in
    direction angle"""

    x, y = coords

    x += amount * math.cos(math.radians(angle))
    y -= amount * math.sin(math.radians(angle))

    return (x, y)
