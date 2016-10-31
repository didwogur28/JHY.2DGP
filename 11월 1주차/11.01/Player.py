from pico2d import *
import random
from Missile import Missile1
from Missile import Missile2
from Missile import Missile3

__author__ = 'user'

Missile1_L = []
Missile2_L = []
Missile3_L = []

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

    LEFT_RUN, RIGHT_RUN, STAND, UP_RUN, DOWN_RUN = 0, 1, 2, 3, 4

    def __init__(self):
        self.x = 400
        self.y = 100
        self.xdir = 0
        self.ydir = 0
        self.LIFE = 1
        self.state = self.STAND
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
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)

        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.x = clamp(50, self.x, 740)
        self.y = clamp(50, self.y, 660)


    def draw(self):
        self.image.clip_draw(self.frame * 110, 0, 110, 118, self.x, self.y)

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.STAND, self.RIGHT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.LEFT_RUN
                self.xdir = -1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.STAND, self.LEFT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.RIGHT_RUN
                self.xdir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.STAND, self.LEFT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.STAND
                self.xdir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.STAND, self.RIGHT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.STAND
                self.xdir = 0

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.STAND, self.UP_RUN, self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.DOWN_RUN
                self.ydir = -1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.STAND, self.DOWN_RUN, self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.UP_RUN
                self.ydir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.STAND, self.DOWN_RUN, self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.STAND
                self.ydir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.STAND, self.UP_RUN, self.LEFT_RUN, self.RIGHT_RUN):
                self.state = self.STAND
                self.ydir = 0

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            newM1 = Missile1(self.x, self.y + 30)
            Missile1_L.append(newM1)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            newM2 = Missile2(self.x, self.y + 30)
            Missile2_L.append(newM2)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_c):
            newM3 = Missile3(self.x, self.y + 30)
            Missile3_L.append(newM3)

