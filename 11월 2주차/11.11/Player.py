from pico2d import *
import random

Missile1_L = []
Missile2_L = []
Missile3_L = []
player = None
class Player:

    PIXEL_PER_METER = (10.0 / 0.1)
    RUN_SPEED_KMPH = 17.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 2.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    image = None

    LEFT_RUN, RIGHT_RUN, IDLE, UP_RUN, DOWN_RUN = 0, 1, 2, 3, 4

    def __init__(self):
        self.x = 400
        self.y = 100
        self.xx = 0
        self.yy = 0
        self.HEART = 1
        self.gage = 5
        self.state = self.IDLE
        self.frame = 0
        self.total_frames = 0.0
        self.life_time = 0.0
        if Player.image == None:
            Player.image = load_image('object/Player/Player.png')

    def update(self,frame_time):
        self.life_time += frame_time
        distance = Player.RUN_SPEED_PPS * frame_time
        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        def barrier(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.x = barrier(50, self.x, 740)
        self.y = barrier(50, self.y, 660)


    def draw(self):
        self.image.clip_draw(self.frame * 110, 0, 110, 118, self.x, self.y)

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.IDLE, self.RIGHT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.LEFT_RUN
                self.xx = -1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.IDLE, self.LEFT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.RIGHT_RUN
                self.xx = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.IDLE, self.LEFT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.IDLE
                self.xx = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.IDLE, self.RIGHT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.IDLE
                self.xx = 0

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.IDLE, self.UP_RUN, self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.DOWN_RUN
                self.yy = -1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.IDLE, self.DOWN_RUN, self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.UP_RUN
                self.yy = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.IDLE, self.DOWN_RUN, self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.IDLE
                self.yy = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.IDLE, self.UP_RUN, self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.IDLE
                self.yy = 0

    def get_missile1(self):
        newM1 = Missile1(self.x, self.y + 50)
        Missile1_L.append(newM1)

    def get_missile2(self):
        newM2 = Missile2(self.x, self.y + 50)
        Missile2_L.append(newM2)

    def get_missile3(self):
        newM3 = Missile3(self.x, self.y + 50)
        Missile3_L.append(newM3)

    def get_bb(self):
        return self.x -30, self.y -50, self.x+30, self.y+30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_bb())

    def life(self, life_down):
        self.gage -= life_down
        if(self.gage <= 0):
            self.HEART = 0
            return self.HAERT
        else:
            return self.HAERT