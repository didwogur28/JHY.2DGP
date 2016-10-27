from pico2d import *
__author__ = 'user'

Missile1_L = []
Missile2_L = []
Missile3_L = []
GrandAttack_L = []

class Missile1:
    PIXEL_PER_METER = (25.0 / 0.1)
    RUN_SPEED_KMPH = 30.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.ydir = 1

    def update(self,frame_time):
        self.image = load_image('object/Missile/Missile1.png')
        distance = Missile1.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

        if(self.x > 750) :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

class Missile2:
    PIXEL_PER_METER = (25.0 / 0.3)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ydir = 1

    def update(self,frame_time):
        self.image = load_image('object/Missile/Missile2.png')
        distance = Missile2.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

        if(self.x > 750) :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

class Missile3:
    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ydir = 1

    def update(self,frame_time):
        self.image = load_image('object/Missile/Missile3.png')
        distance = Missile2.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

        if(self.x > 750) :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

class GrandAttack1:
    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    global ga1
    ga1 = False

    def __init__(self):
        self.x = 200
        self.y = -200
        self.ydir = 1

    def update(self,frame_time):
        self.image = load_image('object/Player/GrateAttack1.png')
        if (ga1 == True):
            distance = GrandAttack1.RUN_SPEED_PPS * frame_time
            self.y += (self.ydir * distance)

        if (self.x > 750):
            return True
        else:
            return False

    def handle_event(self, event):
        global ga1
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            ga1 = True

    def draw(self):
        self.image.draw(self.x, self.y)

class GrandAttack2:
    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    global ga2
    ga2 = False

    def __init__(self):
        self.x = 600
        self.y = -200
        self.ydir = 1

    def update(self,frame_time):
        global ga2
        self.image = load_image('object/Player/GrateAttack2.png')
        if (ga1 == True):
            distance = GrandAttack2.RUN_SPEED_PPS * frame_time
            self.y += (self.ydir * distance)

        if (self.x > 750):
            return True
        else:
            return False

    def handle_event(self, event):
        global ga2
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            ga2 = True

    def draw(self):
        self.image.draw(self.x, self.y)