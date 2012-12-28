win_width =  800
win_height = 600

clear_color = (120, 200, 255)

images = 'images/'

gravity = 2000 # something with inc_y of things

class monkey():
    dimensions = (160, 240)

    mouth_timeout = 150 # ms before mouth opens again after closed

    move_factor = 0.1

    class mouth_tweak():
        ammount = 65
        direction = -65


class arm():
    dimensions = (150, 40)
    position_factor = 0.4

    top_angle = 120
    bottom_angle = 260
    throw_angle =  170
    prepare_factor = 4
    throw_factor = 10
    rotation_error = 5

    # pixels to move the fruit so it fits inside the palm
    class fruit_tweak():
        ammount = 25
        direction = -110

class fruit():
    dimensions = (60, 60)
    rot_inc_max = 360

    min_inc_x = -100
    max_inc_x = -1000
    max_init_inc_y = -550

    shrink = 2 # it shrinks from 1 to 0 when eaten. this parameter is the rate.
    rot_inc_extra = 5 # when shrinking, rotate faster by this factor

class collision():
    fruit_monkey = 40**2

class cloud():
    max_width = 300
    max_height = 140
    min_circles = 2
    max_circles = 6
    min_radius = 75
    max_ix = 20
    delta = (100, 600) # width between clouds

class tree():
    dimensions = (140, 200)
    max_trees = 3
