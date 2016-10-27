from pico2d import *
import random
from Missile import Missile1
from Missile import Missile2
from Missile import Missile3

__author__ = 'user'

class Player:
    global missile1, missile2, missile3
    image = None
    frameSize = 9

    LEFT, RIGHT, IDLE, UP, DOWN, ATTACK = 0, 1, 2, 3, 4, 5

    global rightmove, leftmove, upmove, downmove

    leftmove = False
    rightmove = False
    upmove = False
    downmove = False

    global mis1, mis2, mis3
    mis1 = []
    mis2 = []
    mis3 = []

    missile1 = Missile1(0, 0)
    missile2 = Missile2(0, 0)
    missile3 = Missile3(0, 0)

    def __init__(self):
        self.x = 400
        self.y = 90
        self.xdir = 0
        self.ydir = 0
        self.state = self.IDLE
        self.frame = random.randint(0, 1)
        if Player.image == None:
            Player.image = load_image('object/Player/Player.png')

    def update(self):
        global rightmove, leftmove, upmove, downmove
        global mis1, mis2, mis3
        for ms1 in mis1:
            ms1.update()
        for ms2 in mis2:
            ms2.update()
        for ms3 in mis3:
            ms3.update()

        self.frame = (self.frame + 1) % self.frameSize
        missile1.update()
        missile2.update()
        missile3.update()

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

        self.x += self.xdir
        self.y += self.ydir

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
            mis1.append(Missile1(self.x, self.y + 50))
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            mis2.append(Missile2(self.x, self.y + 50))
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_c):
            mis3.append(Missile3(self.x, self.y + 50))

    def draw(self):
        global ms1, ms2, ms3
        self.image.draw(self.x, self.y)
        for ms1 in mis1:
            ms1.draw()
        for ms2 in mis2:
            ms2.draw()
        for ms3 in mis3:
            ms3.draw()


