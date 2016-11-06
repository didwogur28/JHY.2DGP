import random

import game_framework
import title_state

from Missile import GrandAttack1
from Missile import GrandAttack2

from pico2d import *

name = "MainState"

running = None
player = None
boss = None

Missile1_L = []
Missile2_L = []
Missile3_L = []
E_Missile_L = []

class Map :
    PIXEL_PER_METER = (10.0 / 0.1)
    SCROLL_SPEED_KMPH = 20.0
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.0)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self, w, h) :
        self.image = load_image('object/Canvas/Map.png')
        self.speed = 0
        self.down = 0
        self.screen_width = w
        self.screen_height = h

    def draw(self) :
        y = int (self.down)
        h = min (self.image.h - y, self.screen_height)
        self.image.clip_draw_to_origin(0, y, self.screen_width ,h,0,0)
        self.image.clip_draw_to_origin(0,0,self.screen_width, self.screen_height - h, 0, h)

    def update(self,frame_time):
        self.down = (self.down + frame_time * self.speed) % self.image.h
        self.speed = Map.SCROLL_SPEED_PPS

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
        self.LIFE = 1
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

class Create:
    def __init__(self):
        self.create1 = 0.0
        self.create2 = 0.0
        self.create3 = 0.0
        self.create4 = 0.0
        self.createmiddle = 0.0
        self.createboss = 0.0
        self.middlel = False
        self.bossl = False

    def update(self, frame_time):
        self.create1 += frame_time
        self.create2 += frame_time
        self.create3 += frame_time
        self.create4 += frame_time
        self.createmiddle += frame_time
        self.createboss += frame_time
        self.CEnemyOne()
        self.CEnemyTwo()
        self.CEnemyThree()
        self.CEnemyFour()
        self.CMiddleBoss()
        self.CBoss()

    def CEnemyOne(self):
        if (self.create1 >= 3 and self.bossl == False):
            nEnemyOne = EnemyOne()
            EnemyOne_L.append(nEnemyOne)
            self.create1 = 0.0

    def CEnemyTwo(self):
        if (self.create2 >= 6 and self.bossl == False):
            nEnemyTwo = EnemyTwo()
            EnemyTwo_L.append(nEnemyTwo)
            self.create2 = 0.0

    def CEnemyThree(self):
        if (self.create3 >= 5 and self.bossl == False):
            nEnemyThree = EnemyThree()
            EnemyThree_L.append(nEnemyThree)
            self.create3 = 0.0

    def CEnemyFour(self):
        if (self.create4 >= 6 and self.bossl == False):
            nEnemyFour = EnemyFour()
            EnemyFour_L.append(nEnemyFour)
            self.create4 = 0.0

    def CMiddleBoss(self):
        if (self.createmiddle >= 40 and self.bossl == False):
            self.middlel = True
            nMiddleBoss = MiddleBoss()
            MiddleBoss_L.append(nMiddleBoss)
            self.createmiddle = 0.0

    def CBoss(self):
        if (self.createboss >= 80 and self.bossl == False):
            if self.middlel == True:
                self.middlel = False
            self.bossl = True
            nBoss = Boss()
            Boss_L.append(nBoss)
            self.createboss = 0.0

class EnemyOne:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    EnemyMissile_TIME = 0.5

    DOWN_RUN, UP_RUN, DOWN_IDLE, UP_IDLE = 0, 1, 2, 3

    image = None

    def __init__(self):
        if EnemyOne.image == None:
            EnemyOne.image = load_image('object/Enemy/Enemy1.png')
        self.x, self.y = random.randint(100, 750), random.randint(1000, 1100)
        self.xx = 0
        self.yy = 0
        self.frame = random.randint(0, 4)
        self.run_frame = 0
        self.idle_frame = 0
        self.total_frames = 0.0
        self.missile_c = 0
        self.state = self.DOWN_RUN
        self.name = 'enemyone'

    def handle_down_run(self):
        self.yy = -1
        self.run_frame += 1
        if self.y < 150:
            self.state = self.UP_RUN
            self.y = 150
        if self.run_frame == 60:
            self.state = self.DOWN_IDLE
            self.idle_frame = 0
    def handle_down_idle(self):
        self.idle_frame += 1
        if self.idle_frame == 60:
            self.state = self.DOWN_RUN
            self.run_frame = 0

    def handle_up_run(self):
        self.yy = 1
        self.run_frame += 1
        if self.y  > 700:
            self.state = self.DOWN_RUN
            self.y = 700
        if self.run_frame == 60:
            self.state = self.UP_IDLE
            self.idle_frame = 0
    def handle_up_idle(self):
        self.idle_frame += 1
        if self.idle_frame == 60:
            self.state = self.UP_RUN
            self.run_frame = 0

    handle_state = {
        DOWN_RUN: handle_down_run, UP_RUN: handle_up_run, DOWN_IDLE: handle_down_idle, UP_IDLE: handle_up_idle}

    def update(self,frame_time):
        distance = EnemyOne.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyOne.FRAMES_PER_ACTION * EnemyOne.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)
        self.handle_state[self.state](self)
        self.missile_c += frame_time * self.EnemyMissile_TIME
        if self.missile_c > 1:
            self.missile_c = 0
            e_missile = E_Missile(self.x - 10, self.y - 30)
            E_Missile_L.append(e_missile)

    def draw(self):
        self.image.clip_draw(self.frame * 160, 0, 160, 180, self.x, self.y)

class EnemyTwo:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    E_Missile_Time = 1.0
    LEFTDOWN_RUN, RIGHTUP_RUN, LEFTDOWN_IDLE, RIGHTUP_IDLE = 0, 1, 2, 3

    image = None

    def __init__(self):
        if EnemyTwo.image == None:
            EnemyTwo.image = load_image('object/Enemy/Enemy2.png')
        self.x, self.y = random.randint(800, 1000), random.randint(1000, 1100)
        self.xx = 0
        self.yy = 0
        self.frame = random.randint(0, 6)
        self.run_frame = 0
        self.idle_frame = 0
        self.total_frames = 0.0
        self.missile_c = 0
        self.state = self.LEFTDOWN_RUN
        self.name = 'enemytwo'

    def handle_leftdown_run(self):
        self.xx = -1
        self.yy = -1
        self.run_frame += 1
        if self.y < 100:
            self.state = self.RIGHTUP_RUN
        if self.x < 100:
            self.state = self.RIGHTUP_RUN
        if self.run_frame == 200:
            self.state = self.LEFTDOWN_IDLE
            self.idle_frame = 0
    def handle_leftdown_idle(self):
        self.idle_frame += 1
        if self.idle_frame == 50:
            self.state = self.LEFTDOWN_RUN
            self.run_frame = 0

    def handle_rightup_run(self):
        self.xx = 1
        self.yy = 1
        self.run_frame += 1
        if self.y > 700:
            self.state = self.LEFTDOWN_RUN
        if self.x > 700:
            self.state = self.LEFTDOWN_RUN
        if self.run_frame == 200:
            self.state = self.RIGHTUP_IDLE
            self.idle_frame = 0
    def handle_rightup_idle(self):
        self.idle_frame += 1
        if self.idle_frame == 50:
            self.state = self.RIGHTUP_RUN
            self.run_frame = 0

    handle_state = {
        LEFTDOWN_RUN: handle_leftdown_run, RIGHTUP_RUN: handle_rightup_run,
        LEFTDOWN_IDLE: handle_leftdown_idle, RIGHTUP_IDLE:handle_rightup_idle
        }

    def update(self,frame_time):
        distance = EnemyTwo.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyTwo.FRAMES_PER_ACTION * EnemyTwo.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)
        self.handle_state[self.state](self)
        self.missile_c += frame_time * self.E_Missile_Time
        if self.missile_c > 1:
            self.missile_c = 0
            e_missile = E_Missile(self.x - 10, self.y - 30)
            E_Missile_L.append(e_missile)

    def draw(self):
        self.image.clip_draw(self.frame * 140, 0, 140, 160, self.x, self.y)

class EnemyThree:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    E_Missile_Time = 0.5

    DOWN_RUN, UP_RUN, DOWN_IDLE, UP_IDLE = 0, 1, 2, 3

    image = None

    def __init__(self):
        if EnemyThree.image == None:
            EnemyThree.image = load_image('object/Enemy/Enemy3.png')
        self.x, self.y = random.randint(70, 730), random.randint(1000, 1100)
        self.xx = 0
        self.yy = 0
        self.frame = random.randint(0, 4)
        self.run_frame = 0
        self.idle_frame = 0
        self.total_frames = 0.0
        self.missile_c = 0
        self.state = self.DOWN_RUN
        self.name = 'enemythree'

    def handle_down_run(self):
        self.yy = -1
        self.run_frame += 1
        if self.y < 400:
            self.state = self.UP_RUN
            self.y = 400
        if self.run_frame == 80:
            self.state = self.DOWN_IDLE
            self.idle_frame = 0
    def handle_down_idle(self):
        self.idle_frame += 1
        if self.idle_frame == 80:
            self.state = self.DOWN_RUN
            self.run_frame = 0

    def handle_up_run(self):
        self.yy = 1
        self.run_frame += 1
        if self.y  > 700:
            self.state = self.DOWN_RUN
            self.y = 700
        if self.run_frame == 80:
            self.state = self.UP_IDLE
            self.idle_frame = 0
    def handle_up_idle(self):
        self.idle_frame += 1
        if self.idle_frame == 80:
            self.state = self.UP_RUN
            self.run_frame = 0

    handle_state = {
        DOWN_RUN: handle_down_run, UP_RUN: handle_up_run, DOWN_IDLE: handle_down_idle, UP_IDLE: handle_up_idle}

    def update(self,frame_time):
        distance = EnemyThree.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyThree.FRAMES_PER_ACTION * EnemyThree.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)
        self.handle_state[self.state](self)
        self.missile_c += frame_time * self.E_Missile_Time
        if self.missile_c > 1:
            self.missile_c = 0
            e_missile = E_Missile(self.x - 10, self.y - 30)
            E_Missile_L.append(e_missile)

    def draw(self):
        self.image.clip_draw(self.frame * 120, 0, 120, 120, self.x, self.y)

class EnemyFour:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    E_Missile_Time = 1.0

    RIGHTDOWN_RUN, LEFTUP_RUN, RIGHTDOWN_IDLE, LEFTUP_IDLE = 0, 1, 2, 3

    image = None

    def __init__(self):
        if EnemyFour.image == None:
            EnemyFour.image = load_image('object/Enemy/Enemy2.png')
        self.x, self.y = random.randint(-200, -100), random.randint(1000, 1100)
        self.xx = 0
        self.yy = 0
        self.frame = random.randint(0, 6)
        self.run_frame = 0
        self.idle_frame = 0
        self.total_frames = 0.0
        self.missile_c = 0
        self.state = self.RIGHTDOWN_RUN
        self.name = 'enemyfour'


    def handle_rightdown_run(self):
        self.xx = 1
        self.yy = -1
        self.run_frame += 1
        if self.y < 100:
            self.state = self.LEFTUP_RUN
        if self.x > 700:
            self.state = self.LEFTUP_RUN
        if self.run_frame == 200:
            self.state = self.RIGHTDOWN_IDLE
            self.idle_frame = 0
    def handle_rightdown_idle(self):
        self.idle_frame += 1
        if self.idle_frame == 50:
            self.state = self.RIGHTDOWN_RUN
            self.run_frame = 0

    def handle_leftup_run(self):
        self.xx = -1
        self.yy = 1
        self.run_frame += 1
        if self.y > 700:
            self.state = self.RIGHTDOWN_RUN
        if self.x < 100:
            self.state = self.RIGHTDOWN_RUN
        if self.run_frame == 200:
            self.state = self.LEFTUP_IDLE
            self.idle_frame = 0
    def handle_leftup_idle(self):
        self.idle_frame += 1
        if self.idle_frame == 50:
            self.state = self.LEFTUP_RUN
            self.run_frame = 0

    handle_state = {
        RIGHTDOWN_RUN: handle_rightdown_run, LEFTUP_RUN: handle_leftup_run,
        RIGHTDOWN_IDLE: handle_rightdown_idle, LEFTUP_IDLE: handle_leftup_idle
        }

    def update(self,frame_time):
        distance = EnemyFour.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyFour.FRAMES_PER_ACTION * EnemyFour.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)
        self.handle_state[self.state](self)
        self.missile_c += frame_time * self.E_Missile_Time
        if self.missile_c > 1:
            self.missile_c = 0
            e_missile = E_Missile(self.x - 10, self.y - 30)
            E_Missile_L.append(e_missile)

    def draw(self):
        self.image.clip_draw(self.frame * 140, 0, 140, 160, self.x, self.y)

class MiddleBoss:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    DOWN_IDLE = 0
    def __init__(self):
        self.x, self.y = 400, 1000
        self.xx = 0
        self.yy = 0
        self.frame = random.randint(0,7)
        self.run_frame = 0
        self.idle_frame = 0
        self.total_frames = 0.0
        self.name = 'middleboss'
        self.state  =  self.DOWN_IDLE
        if MiddleBoss.image == None:
            MiddleBoss.image = load_image('object/Enemy/MiddleBoss.png')

    def handle_down_idle(self):
        self.yy = -1
        if self.y < 580:
            self.yy = 0
            self.state = self.DOWN_IDLE

    handle_state = {
            DOWN_IDLE: handle_down_idle
    }

    def update(self,frame_time):
        distance = MiddleBoss.RUN_SPEED_PPS * frame_time
        self.total_frames += MiddleBoss.FRAMES_PER_ACTION * MiddleBoss.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)
        self.handle_state[self.state](self)

    def draw(self):
             self.image.clip_draw(self.frame * 320, 0, 320, 390, self.x, self.y)

class Boss:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    DOWN_IDLE = 0
    def __init__(self):
        self.x, self.y = 400, 1200
        self.xx = 0
        self.yy = 0
        self.frame = random.randint(0,7)
        self.run_frame = 0
        self.idle_frame = 0
        self.total_frames = 0.0
        self.state  =  self.DOWN_IDLE
        self.name = 'boss'
        if Boss.image == None:
            Boss.image = load_image('object/Enemy/Boss.png')

    def handle_down_idle(self):
        self.yy= -1
        if self.y < 580:
            self.yy = 0
            self.state = self.DOWN_IDLE

    handle_state = {
            DOWN_IDLE: handle_down_idle
    }

    def update(self,frame_time):
        distance = Boss.RUN_SPEED_PPS * frame_time
        self.total_frames += Boss.FRAMES_PER_ACTION * Boss.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)
        self.handle_state[self.state](self)

    def draw(self):
             self.image.clip_draw(self.frame * 420, 0, 420, 300, self.x, self.y)

class E_Missile:
    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yy = -1
        if E_Missile.image == None:
            E_Missile.image = load_image('object/Missile/EnemyMissile.png')

    def update(self, frame_time):
        distance = E_Missile.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if (self.y < -10) :
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

class Missile1:
    PIXEL_PER_METER = (25.0 / 0.1)
    RUN_SPEED_KMPH = 30.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        if Missile1.image == None:
            self.image = load_image('object/Missile/Missile1.png')
        self.x = x
        self.y = y
        self.yy = 1

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_z:
            player.get_missile1()

    def update(self,frame_time):
        distance = Missile1.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if(self.y > 750) :
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

    image = None

    def __init__(self, x, y):
        if Missile2.image == None:
            self.image = load_image('object/Missile/Missile2.png')
        self.x = x
        self.y = y
        self.yy = 1

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_x:
            player.get_missile2()

    def update(self,frame_time):
        distance = Missile2.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if(self.y > 750) :
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

    image = None

    def __init__(self, x, y):
        if Missile3.image == None:
            self.image = load_image('object/Missile/Missile3.png')
        self.x = x
        self.y = y
        self.yy = 1

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_c:
            player.get_missile3()

    def update(self,frame_time):
        distance = Missile3.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if(self.y > 750) :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        else:
            player.handle_event(event)
            ga1.handle_events(event)
            ga2.handle_events(event)
            missile1.handle_events(event)
            missile2.handle_events(event)
            missile3.handle_events(event)

def enter():
    global create, map, player, ga1, ga2, EnemyOne_L, EnemyTwo_L, EnemyThree_L, EnemyFour_L, E_Missile_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L, Missile3_L
    game_framework.reset_time()
    map = Map(800, 750)

    create = Create()
    player = Player()

    missile1 = Missile1(0,0)
    missile2 = Missile2(0,0)
    missile3 = Missile3(0,0)

    ga1 = GrandAttack1()
    ga2 = GrandAttack2()

    Missile1_L = []
    Missile2_L = []
    Missile3_L = []
    E_Missile_L = []
    EnemyOne_L = []
    EnemyTwo_L = []
    EnemyThree_L = []
    EnemyFour_L = []
    MiddleBoss_L = []
    Boss_L = []

def exit():
    global create, map, player, ga1, ga2, EnemyOne_L,EnemyTwo_L, EnemyThree_L, EnemyFour_L, E_Missile_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L, Missile3_L
    del(create)
    del(player)
    del(Missile1_L)
    del(Missile2_L)
    del(Missile3_L)
    del(EnemyOne_L)
    del(EnemyTwo_L)
    del(EnemyThree_L)
    del(EnemyFour_L)
    del(E_Missile_L)
    del(MiddleBoss_L)
    del(Boss_L)
    del(ga1)
    del(ga2)
    del(missile1)
    del(missile2)
    del(missile3)
    del(map)
    close_canvas()

def update(frame_time):
    create.update(frame_time)
    map.update(frame_time)
    player.update(frame_time)

    ga1.update(frame_time)
    ga2.update(frame_time)

    for missile1 in Missile1_L:
        missile1.update(frame_time)
        out = missile1.update(frame_time)
        if out == True:
            Missile1_L.remove(missile1)
    for missile2 in Missile2_L:
        missile2.update(frame_time)
        out = missile2.update(frame_time)
        if out == True:
            Missile2_L.remove(missile2)
    for missile3 in Missile3_L:
        missile3.update(frame_time)
        out = missile3.update(frame_time)
        if out == True:
            Missile3_L.remove(missile3)
    for e_missile in E_Missile_L:
        e_missile.update(frame_time)
        out = e_missile.update(frame_time)
        if out == True:
            E_Missile_L.remove(e_missile)

    for enemyone in EnemyOne_L:
        enemyone.update(frame_time)
    for enemytwo in EnemyTwo_L:
        enemytwo.update(frame_time)
    for enemythree in EnemyThree_L:
        enemythree.update(frame_time)
    for enemyfour in EnemyFour_L:
        enemyfour.update(frame_time)
    for middleboss in MiddleBoss_L:
        middleboss.update(frame_time)
    for boss in Boss_L:
        boss.update(frame_time)

def draw(frame_time):
    clear_canvas()
    map.draw()

    for enemyone in EnemyOne_L:
        enemyone.draw()
    for enemytwo in EnemyTwo_L:
        enemytwo.draw()
    for enemythree in EnemyThree_L:
        enemythree.draw()
    for enemyfour in EnemyFour_L:
        enemyfour.draw()
    for middleboss in MiddleBoss_L:
        middleboss.draw()
    for boss in Boss_L:
        boss.draw()

    player.draw()

    for missile1 in Missile1_L:
        missile1.draw()
    for missile2 in Missile2_L:
        missile2.draw()
    for missile3 in Missile3_L:
        missile3.draw()

    for e_missile in E_Missile_L:
        e_missile.draw()

    ga1.draw()
    ga2.draw()

    update_canvas()
