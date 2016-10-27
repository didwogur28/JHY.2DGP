from pico2d import *
import random
from Missile import Missile1
from Missile import Missile2
from Missile import Missile3

__author__ = 'user'

class Player:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 2.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = None
    frameSize = 9

    LEFT, RIGHT, IDLE, UP, DOWN, ATTACK = 0, 1, 2, 3, 4, 5

    leftmove = False
    rightmove = False
    upmove = False
    downmove = False


    Missile1_L = []
    Missile2_L = []
    Missile3_L = []

    def __init__(self):
        self.x = 400
        self.y = 90
        self.xdir = 0
        self.ydir = 0
        self.state = self.IDLE
        self.frame = 0
        self.total_frames = 0.0
        if Player.image == None:
            Player.image = load_image('object/Player/Player.png')

    def update(self, frame_time):
        distance = Player.RUN_SPEED_PPS * frame_time
        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)

        ms1 = Missile1(0, 0)
        ms2 = Missile2(0, 0)
        ms3 = Missile3(0, 0)

        global rightmove, leftmove, upmove, downmove
        global Missile1_L, Missile2_L, Missile3_L
        for ms1 in Missile1_L:
            ms1.update(frame_time)
            out =  ms1.update(frame_time)
            if out == True:
                Missile1_L.remove(ms1)
        for ms2 in Missile2_L:
            ms2.update(frame_time)
            out = ms2.update(frame_time)
            if out == True:
                Missile2_L.remove(ms2)
        for ms3 in Missile3_L:
            ms3.update(frame_time)
            out = ms3.update(frame_time)
            if out == True:
                Missile3_L.remove(ms3)

        ms1.update(frame_time)
        ms2.update(frame_time)
        ms3.update(frame_time)

        self.frame = (self.frame + 1) % self.frameSize

        if (rightmove == True):
            self.x += 10
            if(upmove == True):
                self.x += 10
                self.y += 10
            elif(downmove == True):
                self.x += 10
                self.y -= 10
        elif (leftmove == True):
            self.x -= 10
            if (upmove == True):
                self.x -= 10
                self.y += 10
            elif (downmove == True):
                self.x -= 10
                self.y -= 10
        elif (upmove == True):
            self.y += 10
            if (rightmove == True):
                self.y += 10
                self.x += 10
            elif (leftmove == True):
                self.y += 10
                self.x -= 10
        elif (downmove == True):
            self.y -= 10
            if (rightmove == True):
                self.y -= 10
                self.x += 10
            elif (leftmove == True):
                self.y -= 10
                self.x -= 10

        def clamp(minimum, y, maximum):
            return max(minimum, min(y, maximum))
        self.x = clamp(50, self.x, 750)
        self.y = clamp(50, self.y, 650)

    def handle_event(self, event):
        global leftmove, rightmove, upmove, downmove
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            rightmove = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            leftmove = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            upmove = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            downmove = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            rightmove = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            leftmove = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            upmove = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            downmove = False

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            Missile1_L.append(Missile1(self.x, self.y + 50))
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            Missile2_L.append(Missile2(self.x, self.y + 50))
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_c):
            Missile3_L.append(Missile3(self.x, self.y + 50))

    def draw(self):
        global ms1, ms2, ms3
        self.image.draw(self.x, self.y)
        for ms1 in Missile1_L:
            ms1.draw()
        for ms2 in Missile2_L:
            ms2.draw()
        for ms3 in Missile3_L:
            ms3.draw()


