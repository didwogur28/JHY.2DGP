from pico2d import *

__author__ = 'user'

class GrandAttack1:

    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = None

    def __init__(self):
        self.x, self.y = 200, -200
        self.yy = 0
        self.grandattack1 = 0
        self.countga1 = 3
        if GrandAttack1.image == None:
            GrandAttack1.image = load_image('object/Player/GrateAttack1.png')

    def update(self,frame_time):
        distance = GrandAttack1.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

    def handle_events(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            self.grandattack1 = 1
            self.yy = 1
            if self.grandattack1 == 1:
                if self.y > 1000:
                    self.grandattack1 = 0
                    self.y = -200
                self.countga1 -= 1
            if self.countga1 < 0:
                self.countga1 = 0
                self.yy = 0


    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 200, self.y -130, self.x + 250, self.y + 150

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class GrandAttack2:
    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = None

    def __init__(self):
        self.x, self.y = 600, -200
        self.yy = 0
        self.grandattack2 = 0
        self.countga2 = 3
        if GrandAttack2.image == None:
            GrandAttack2.image = load_image('object/Player/GrateAttack2.png')

    def update(self,frame_time):
        distance = GrandAttack2.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

    def handle_events(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            self.grandattack2 = 1
            self.yy = 1
            if self.grandattack2 == 1:
                if self.y > 1000:
                    self.grandattack2 = 0
                    self.y = -200
                self.countga2 -=1
            if self.countga2 < 0:
                self.countga2 = 0
                self.yy = 0

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 250, self.y -130, self.x + 200, self.y + 150

    def draw_bb(self):
        draw_rectangle(*self.get_bb())