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
MD_Missile_L = []
B_Missile_L = []
Blast_L = []

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
            return self.HEART
        else:
            return self.HEART

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
        if (self.createboss >= 75 and self.bossl == False):
            if self.middlel == True:
                self.middlel = False
            self.bossl = True
            nBoss = Boss()
            Boss_L.append(nBoss)
            self.createboss = 0.0


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a > bottom_b : return False
    if bottom_a > top_b : return False
    return True

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
        self.HEART = True
        self.gage = 200
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

    def get_bb(self):
        return self.x -60, self.y -20, self.x +70, self.y +30
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def life(self, life_down):
        self.gage -= life_down
        if(self.gage < 0):
            self.HEART = False
            return self.HEART
        else:
            return self.HEART

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
        self.HEART = True
        self.gage = 100
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

    def get_bb(self):
        return self.x -25, self.y -40, self.x +25, self.y +50
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def life(self, life_down):
        self.gage -= life_down
        if(self.gage < 0):
            self.HEART = False
            return self.HEART
        else:
            return self.HEART


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
        self.HEART = True
        self.gage = 150
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

    def get_bb(self):
        return self.x -25, self.y -40, self.x +20, self.y +50
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def life(self, life_down):
        self.gage -= life_down
        if(self.gage < 0):
            self.HEART = False
            return self.HEART
        else:
            return self.HEART

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
        self.HEART = True
        self.gage = 150
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

    def get_bb(self):
        return self.x -25, self.y -40, self.x +25, self.y +50
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def life(self, life_down):
        self.gage -= life_down
        if(self.gage < 0):
            self.HEART = False
            return self.HEART
        else:
            return self.HEART

class MiddleBoss:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    E_Missile_Time = 0.3

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
        self.missile_c = 0
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
        self.missile_c += frame_time * self.E_Missile_Time
        if self.missile_c > 1:
            self.missile_c = 0
            md_missile1 = MD_Missile(self.x , self.y - 30)
            md_missile2 = MD_Missile(self.x , self.y - 60)
            md_missile3 = MD_Missile(self.x , self.y - 90)
            md_missile4 = MD_Missile(self.x , self.y - 120)
            md_missile5 = MD_RMissile(self.x + 40, self.y - 30)
            md_missile6 = MD_RMissile(self.x + 60, self.y - 60)
            md_missile7 = MD_RMissile(self.x + 80, self.y - 90)
            md_missile8 = MD_RMissile(self.x + 100, self.y - 120)
            md_missile9 = MD_RRMissile(self.x + 20, self.y - 30)
            md_missile10 = MD_RRMissile(self.x + 30, self.y - 60)
            md_missile11 = MD_RRMissile(self.x + 40, self.y - 90)
            md_missile12 = MD_RRMissile(self.x + 50, self.y - 120)
            md_missile13 = MD_LMissile(self.x - 40, self.y - 30)
            md_missile14 = MD_LMissile(self.x - 60, self.y - 60)
            md_missile15 = MD_LMissile(self.x - 80, self.y - 90)
            md_missile16 = MD_LMissile(self.x - 100, self.y - 120)
            md_missile17 = MD_LLMissile(self.x - 20, self.y - 30)
            md_missile18 = MD_LLMissile(self.x - 30, self.y - 60)
            md_missile19 = MD_LLMissile(self.x - 40, self.y - 90)
            md_missile20 = MD_LLMissile(self.x - 50, self.y - 120)

            MD_Missile_L.append(md_missile1)
            MD_Missile_L.append(md_missile2)
            MD_Missile_L.append(md_missile3)
            MD_Missile_L.append(md_missile4)
            MD_Missile_L.append(md_missile5)
            MD_Missile_L.append(md_missile6)
            MD_Missile_L.append(md_missile7)
            MD_Missile_L.append(md_missile8)
            MD_Missile_L.append(md_missile9)
            MD_Missile_L.append(md_missile10)
            MD_Missile_L.append(md_missile11)
            MD_Missile_L.append(md_missile12)
            MD_Missile_L.append(md_missile13)
            MD_Missile_L.append(md_missile14)
            MD_Missile_L.append(md_missile15)
            MD_Missile_L.append(md_missile16)
            MD_Missile_L.append(md_missile17)
            MD_Missile_L.append(md_missile18)
            MD_Missile_L.append(md_missile19)
            MD_Missile_L.append(md_missile20)

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

    E_Missile_Time = 0.3

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
        self.missile_c = 0
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
        self.missile_c += frame_time * self.E_Missile_Time
        if self.missile_c > 1:
            self.missile_c = 0
            b_missile1 = B_RMissile(self.x + 90, self.y - 30)
            b_missile2 = B_RMissile(self.x + 110, self.y - 60)
            b_missile3 = B_RMissile(self.x + 130, self.y - 90)
            b_missile4 = B_RMissile(self.x + 150, self.y - 120)
            b_missile5 = B_RMissile(self.x + 170, self.y - 150)
            b_missile6 = B_RMissile(self.x + 190, self.y - 180)
            b_missile7 = B_RRMissile(self.x + 70, self.y - 30)
            b_missile8 = B_RRMissile(self.x + 85, self.y - 60)
            b_missile9 = B_RRMissile(self.x + 100, self.y - 90)
            b_missile10 = B_RRMissile(self.x + 115, self.y - 120)
            b_missile11 = B_RRMissile(self.x + 130, self.y - 150)
            b_missile12 = B_RRMissile(self.x + 145, self.y - 180)
            b_missile13 = B_RRRMissile(self.x + 50, self.y - 30)
            b_missile14 = B_RRRMissile(self.x + 60, self.y - 60)
            b_missile15 = B_RRRMissile(self.x + 70, self.y - 90)
            b_missile16 = B_RRRMissile(self.x + 80, self.y - 120)
            b_missile17 = B_RRRMissile(self.x + 90, self.y - 150)
            b_missile18 = B_RRRMissile(self.x + 100, self.y - 180)
            b_missile19 = B_RRRRMissile(self.x + 30, self.y - 30)
            b_missile20 = B_RRRRMissile(self.x + 35, self.y - 60)
            b_missile21 = B_RRRRMissile(self.x + 40, self.y - 90)
            b_missile22 = B_RRRRMissile(self.x + 45, self.y - 120)
            b_missile23 = B_RRRRMissile(self.x + 50, self.y - 150)
            b_missile24 = B_RRRRMissile(self.x + 55, self.y - 180)

            b_missile25 = B_LMissile(self.x - 90, self.y - 30)
            b_missile26 = B_LMissile(self.x - 110, self.y - 60)
            b_missile27 = B_LMissile(self.x - 130, self.y - 90)
            b_missile28 = B_LMissile(self.x - 150, self.y - 120)
            b_missile29 = B_LMissile(self.x - 170, self.y - 150)
            b_missile30 = B_LMissile(self.x - 190, self.y - 180)
            b_missile31 = B_LLMissile(self.x - 70, self.y - 30)
            b_missile32 = B_LLMissile(self.x - 85, self.y - 60)
            b_missile33 = B_LLMissile(self.x - 100, self.y - 90)
            b_missile34 = B_LLMissile(self.x - 115, self.y - 120)
            b_missile35 = B_LLMissile(self.x - 130, self.y - 150)
            b_missile36 = B_LLMissile(self.x - 145, self.y - 180)
            b_missile37 = B_LLLMissile(self.x - 50, self.y - 30)
            b_missile38 = B_LLLMissile(self.x - 60, self.y - 60)
            b_missile39 = B_LLLMissile(self.x - 70, self.y - 90)
            b_missile40 = B_LLLMissile(self.x - 80, self.y - 120)
            b_missile41 = B_LLLMissile(self.x - 90, self.y - 150)
            b_missile42 = B_LLLMissile(self.x - 100, self.y - 180)
            b_missile43 = B_LLLLMissile(self.x - 30, self.y - 30)
            b_missile44 = B_LLLLMissile(self.x - 35, self.y - 60)
            b_missile45 = B_LLLLMissile(self.x - 40, self.y - 90)
            b_missile46 = B_LLLLMissile(self.x - 45, self.y - 120)
            b_missile47 = B_LLLLMissile(self.x - 50, self.y - 150)
            b_missile48 = B_LLLLMissile(self.x - 55, self.y - 180)

            B_Missile_L.append(b_missile1), B_Missile_L.append(b_missile2), B_Missile_L.append(b_missile3), B_Missile_L.append(b_missile4)
            B_Missile_L.append(b_missile5), B_Missile_L.append(b_missile6), B_Missile_L.append(b_missile7), B_Missile_L.append(b_missile8)
            B_Missile_L.append(b_missile9), B_Missile_L.append(b_missile10), B_Missile_L.append(b_missile11), B_Missile_L.append(b_missile12)
            B_Missile_L.append(b_missile13), B_Missile_L.append(b_missile14), B_Missile_L.append(b_missile15), B_Missile_L.append(b_missile16)
            B_Missile_L.append(b_missile17), B_Missile_L.append(b_missile18), B_Missile_L.append(b_missile19), B_Missile_L.append(b_missile20)
            B_Missile_L.append(b_missile21), B_Missile_L.append(b_missile22), B_Missile_L.append(b_missile23), B_Missile_L.append(b_missile24)
            B_Missile_L.append(b_missile25), B_Missile_L.append(b_missile26), B_Missile_L.append(b_missile27), B_Missile_L.append(b_missile28)
            B_Missile_L.append(b_missile29), B_Missile_L.append(b_missile30), B_Missile_L.append(b_missile31), B_Missile_L.append(b_missile32)
            B_Missile_L.append(b_missile33), B_Missile_L.append(b_missile34), B_Missile_L.append(b_missile35), B_Missile_L.append(b_missile36)
            B_Missile_L.append(b_missile37), B_Missile_L.append(b_missile38), B_Missile_L.append(b_missile39), B_Missile_L.append(b_missile40)
            B_Missile_L.append(b_missile41), B_Missile_L.append(b_missile42), B_Missile_L.append(b_missile43), B_Missile_L.append(b_missile44)
            B_Missile_L.append(b_missile45), B_Missile_L.append(b_missile46), B_Missile_L.append(b_missile47), B_Missile_L.append(b_missile48)



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

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class MD_Missile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yy = -1
        if MD_Missile.image == None:
            MD_Missile.image = load_image('object/Missile/EnemyMissile.png')

    def update(self, frame_time):
        distance = MD_Missile.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if (self.y < -10) :
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class MD_RMissile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = 0.5
        self.yy = -1

        if MD_RMissile.image == None:
            MD_RMissile.image = load_image('object/Missile/EnemyMissileR.png')

    def update(self, frame_time):
        distance = MD_RMissile.RUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10) :
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class MD_RRMissile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = 0.25
        self.yy = -1

        if MD_RRMissile.image == None:
            MD_RRMissile.image = load_image('object/Missile/EnemyMissileR.png')

    def update(self, frame_time):
        distance = MD_RRMissile.RUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10) :
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class MD_LMissile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = -0.5
        self.yy = -1
        if MD_LMissile.image == None:
            MD_LMissile.image = load_image('object/Missile/EnemyMissileL.png')

    def update(self, frame_time):
        distance = MD_LMissile.RUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10) :
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class MD_LLMissile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = -0.25
        self.yy = -1
        if MD_LLMissile.image == None:
            MD_LLMissile.image = load_image('object/Missile/EnemyMissileL.png')

    def update(self, frame_time):
        distance = MD_LLMissile.RUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10) :
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class B_RMissile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = 0.25
        self.yy = -0.5

        if B_RMissile.image == None:
            B_RMissile.image = load_image('object/Missile/EnemyMissileR.png')

    def update(self, frame_time):
        distance = B_RMissile.RUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class B_RRMissile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = 0.125
        self.yy = -0.5

        if B_RRMissile.image == None:
            B_RRMissile.image = load_image('object/Missile/EnemyMissileRR.png')

    def update(self, frame_time):
        distance = B_RRMissile.RUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class B_RRRMissile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = 0.0625
        self.yy = -0.5

        if B_RRRMissile.image == None:
            B_RRRMissile.image = load_image('object/Missile/EnemyMissileRRR.png')

    def update(self, frame_time):
        distance = B_RRRMissile.RUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class B_RRRRMissile:
    PIXEL_PER_METER = (15.0 / 0.5)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = 0.03125
        self.yy = -0.5

        if B_RRRRMissile.image == None:
            B_RRRRMissile.image = load_image('object/Missile/EnemyMissileRRRR.png')

    def update(self, frame_time):
        distance = B_RRRRMissile.RUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class B_LMissile:
    PIXEL_PEL_METEL = (15.0 / 0.5)
    LUN_SPEED_KMPH = 10.0
    LUN_SPEED_MPM = (LUN_SPEED_KMPH * 1000.0 / 60.0)
    LUN_SPEED_MPS = (LUN_SPEED_MPM / 60.0)
    LUN_SPEED_PPS = (LUN_SPEED_MPS * PIXEL_PEL_METEL)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = -0.25
        self.yy = -0.5

        if B_LMissile.image == None:
            B_LMissile.image = load_image('object/Missile/EnemyMissileL.png')

    def update(self, frame_time):
        distance = B_LMissile.LUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class B_LLMissile:
    PIXEL_PEL_METEL = (15.0 / 0.5)
    LUN_SPEED_KMPH = 10.0
    LUN_SPEED_MPM = (LUN_SPEED_KMPH * 1000.0 / 60.0)
    LUN_SPEED_MPS = (LUN_SPEED_MPM / 60.0)
    LUN_SPEED_PPS = (LUN_SPEED_MPS * PIXEL_PEL_METEL)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = -0.125
        self.yy = -0.5

        if B_LLMissile.image == None:
            B_LLMissile.image = load_image('object/Missile/EnemyMissileLL.png')

    def update(self, frame_time):
        distance = B_LLMissile.LUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class B_LLLMissile:
    PIXEL_PEL_METEL = (15.0 / 0.5)
    LUN_SPEED_KMPH = 10.0
    LUN_SPEED_MPM = (LUN_SPEED_KMPH * 1000.0 / 60.0)
    LUN_SPEED_MPS = (LUN_SPEED_MPM / 60.0)
    LUN_SPEED_PPS = (LUN_SPEED_MPS * PIXEL_PEL_METEL)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = -0.0625
        self.yy = -0.5

        if B_LLLMissile.image == None:
            B_LLLMissile.image = load_image('object/Missile/EnemyMissileLLL.png')

    def update(self, frame_time):
        distance = B_LLLMissile.LUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class B_LLLLMissile:
    PIXEL_PEL_METEL = (15.0 / 0.5)
    LUN_SPEED_KMPH = 10.0
    LUN_SPEED_MPM = (LUN_SPEED_KMPH * 1000.0 / 60.0)
    LUN_SPEED_MPS = (LUN_SPEED_MPM / 60.0)
    LUN_SPEED_PPS = (LUN_SPEED_MPS * PIXEL_PEL_METEL)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = -0.03125
        self.yy = -0.5

        if B_LLLLMissile.image == None:
            B_LLLLMissile.image = load_image('object/Missile/EnemyMissileLLLL.png')

    def update(self, frame_time):
        distance = B_LLLLMissile.LUN_SPEED_PPS * frame_time
        self.x += (self.xx * distance)
        self.y += (self.yy * distance)

        if (self.y < -10):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -20, self.x + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

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

    def get_bb(self):
        return self.x - 10, self.y -15, self.x + 10, self.y + 15

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

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

    def get_bb(self):
        return self.x - 10, self.y -15, self.x + 10, self.y + 15

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

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

    def get_bb(self):
        return self.x - 10, self.y -15, self.x + 10, self.y + 15

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Blast:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 12

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.total_frame = 0.0
        self.life_time = 0.0
        self.image = load_image('object/Missile/Blast.png')

    def update(self, frame_time):
        self.life_time += frame_time
        self.total_frame += Blast.FRAMES_PER_ACTION * Blast.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frame) % 12
        if (self.frame == 11):
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 100,0, 100, 150, self.x, self.y)

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
    global create, map, player, ga1, ga2, EnemyOne_L, EnemyTwo_L, EnemyThree_L, EnemyFour_L, E_Missile_L, MD_Missile_L, B_Missile_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L, Missile3_L, Blast_L
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
    MD_Missile_L = []
    B_Missile_L = []
    EnemyOne_L = []
    EnemyTwo_L = []
    EnemyThree_L = []
    EnemyFour_L = []
    MiddleBoss_L = []
    Boss_L = []
    Blast_L = []

def exit():
    global create, map, player, ga1, ga2, EnemyOne_L,EnemyTwo_L, EnemyThree_L, EnemyFour_L, E_Missile_L, MD_Missile_L, B_Missile_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L, Missile3_L, Blast_L
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
    del(MD_Missile_L)
    del(MiddleBoss_L)
    del(Boss_L)
    del (Blast_L)
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
    if (player.HEART == 1):
        player.update(frame_time)

    ga1.update(frame_time)
    ga2.update(frame_time)

    for blast in Blast_L:
        blast.update(frame_time)
        finish_blast = blast.update(frame_time)
        if finish_blast == True:
            Blast_L.remove(blast)

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
    for md_missile in MD_Missile_L:
        md_missile.update(frame_time)
        out = md_missile.update(frame_time)
        if out == True:
            MD_Missile_L.remove(md_missile)
    for md_Rmissile in MD_Missile_L:
        md_Rmissile.update(frame_time)
        out = md_Rmissile.update(frame_time)
        if out == True:
            MD_Missile_L.remove(md_Rmissile)
    for md_RRmissile in MD_Missile_L:
        md_RRmissile.update(frame_time)
        out = md_RRmissile.update(frame_time)
        if out == True:
            MD_Missile_L.remove(md_RRmissile)
    for md_Lmissile in MD_Missile_L:
        md_Lmissile.update(frame_time)
        out = md_Lmissile.update(frame_time)
        if out == True:
            MD_Missile_L.remove(md_Lmissile)
    for md_LLmissile in MD_Missile_L:
        md_LLmissile.update(frame_time)
        out = md_LLmissile.update(frame_time)
        if out == True:
            MD_Missile_L.remove(md_LLmissile)

    for b_Rmissile in B_Missile_L:
        b_Rmissile.update(frame_time)
        out = b_Rmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_Rmissile)
    for b_RRmissile in B_Missile_L:
        b_RRmissile.update(frame_time)
        out = b_RRmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_RRmissile)
    for b_RRRmissile in B_Missile_L:
        b_RRRmissile.update(frame_time)
        out = b_RRRmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_RRRmissile)
    for b_RRRRmissile in B_Missile_L:
        b_RRRRmissile.update(frame_time)
        out = b_RRRRmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_RRRRmissile)
    for b_Lmissile in B_Missile_L:
        b_Lmissile.update(frame_time)
        out = b_Lmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_Lmissile)
    for b_LLmissile in B_Missile_L:
        b_LLmissile.update(frame_time)
        out = b_LLmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_LLmissile)
    for b_LLLmissile in B_Missile_L:
        b_LLLmissile.update(frame_time)
        out = b_LLLmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_LLLmissile)
    for b_LLLLmissile in B_Missile_L:
        b_LLLLmissile.update(frame_time)
        out = b_LLLLmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_LLLLmissile)

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

    for enemyone in EnemyOne_L:
        if collide(enemyone, player):
            if (player.HEART == 1):
                EnemyOne_L.remove(enemyone)
                player.life(1)
    for enemytwo in EnemyTwo_L:
        if collide(enemytwo, player):
            if (player.HEART == 1):
                EnemyTwo_L.remove(enemytwo)
                player.life(1)
    for enemythree in EnemyThree_L:
        if collide(enemythree, player):
            if (player.HEART == 1):
                EnemyThree_L.remove(enemythree)
                player.life(1)
    for enemyfour in EnemyFour_L:
        if collide(enemyfour, player):
            if (player.HEART == 1):
                EnemyFour_L.remove(enemyfour)
                player.life(1)

    for missile1 in Missile1_L:
        for enemyone in EnemyOne_L:
            if collide(missile1, enemyone):
                enemyone.life(1)
                if (enemyone.HEART == False):
                    EnemyOne_L.remove(enemyone)
                    enemyone_blast = Blast(enemyone.x, enemyone.y)
                    Blast_L.append(enemyone_blast)
    for missile1 in Missile1_L:
        for enemytwo in EnemyTwo_L:
            if collide(missile1, enemytwo):
                enemytwo.life(1)
                if (enemytwo.HEART == False):
                    EnemyTwo_L.remove(enemytwo)
                    enemytwo_blast = Blast(enemytwo.x, enemytwo.y)
                    Blast_L.append(enemytwo_blast)
    for missile1 in Missile1_L:
        for enemythree in EnemyThree_L:
            if collide(missile1, enemythree):
                enemythree.life(1)
                if (enemythree.HEART == False):
                    EnemyThree_L.remove(enemythree)
                    enemythree_blast = Blast(enemythree.x, enemythree.y)
                    Blast_L.append(enemythree_blast)
    for missile1 in Missile1_L:
        for enemyfour in EnemyFour_L:
            if collide(missile1, enemyfour):
                enemyfour.life(1)
                if (enemyfour.HEART == False):
                    EnemyFour_L.remove(enemyfour)
                    enemyfour_blast = Blast(enemyfour.x, enemyfour.y)
                    Blast_L.append(enemyfour_blast)

    for missile2 in Missile2_L:
        for enemyone in EnemyOne_L:
            if collide(missile2, enemyone):
                enemyone.life(1)
                if (enemyone.HEART == False):
                    EnemyOne_L.remove(enemyone)
                    enemyone_blast = Blast(enemyone.x, enemyone.y)
                    Blast_L.append(enemyone_blast)
    for missile2 in Missile2_L:
        for enemytwo in EnemyTwo_L:
            if collide(missile2, enemytwo):
                enemytwo.life(1)
                if (enemytwo.HEART == False):
                    EnemyTwo_L.remove(enemytwo)
                    enemytwo_blast = Blast(enemytwo.x, enemytwo.y)
                    Blast_L.append(enemytwo_blast)
    for missile2 in Missile2_L:
        for enemythree in EnemyThree_L:
            if collide(missile2, enemythree):
                enemythree.life(1)
                if (enemythree.HEART == False):
                    EnemyThree_L.remove(enemythree)
                    enemythree_blast = Blast(enemythree.x, enemythree.y)
                    Blast_L.append(enemythree_blast)
    for missile2 in Missile2_L:
        for enemyfour in EnemyFour_L:
            if collide(missile2, enemyfour):
                enemyfour.life(1)
                if (enemyfour.HEART == False):
                    EnemyFour_L.remove(enemyfour)
                    enemyfour_blast = Blast(enemyfour.x, enemyfour.y)
                    Blast_L.append(enemyfour_blast)

    for missile3 in Missile3_L:
        for enemyone in EnemyOne_L:
            if collide(missile3, enemyone):
                enemyone.life(1)
                if (enemyone.HEART == False):
                    EnemyOne_L.remove(enemyone)
                    enemyone_blast = Blast(enemyone.x, enemyone.y)
                    Blast_L.append(enemyone_blast)
    for missile3 in Missile3_L:
        for enemytwo in EnemyTwo_L:
            if collide(missile3, enemytwo):
                enemytwo.life(1)
                if (enemytwo.HEART == False):
                    EnemyTwo_L.remove(enemytwo)
                    enemytwo_blast = Blast(enemytwo.x, enemytwo.y)
                    Blast_L.append(enemytwo_blast)
    for missile3 in Missile3_L:
        for enemythree in EnemyThree_L:
            if collide(missile3, enemythree):
                enemythree.life(1)
                if (enemythree.HEART == False):
                    EnemyThree_L.remove(enemythree)
                    enemythree_blast = Blast(enemythree.x, enemythree.y)
                    Blast_L.append(enemythree_blast)
    for missile3 in Missile3_L:
        for enemyfour in EnemyFour_L:
            if collide(missile3, enemyfour):
                enemyfour.life(1)
                if (enemyfour.HEART == False):
                    EnemyFour_L.remove(enemyfour)
                    enemyfour_blast = Blast(enemyfour.x, enemyfour.y)
                    Blast_L.append(enemyfour_blast)

    for e_missile in E_Missile_L:
        if collide(e_missile, player):
            if (player.HEART == 1):
                E_Missile_L.remove(e_missile)
                player.life(1)
    for md_missile in MD_Missile_L:
        if collide(md_missile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_missile)
                player.life(1)
    for md_Rmissile in MD_Missile_L:
        if collide(md_Rmissile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_Rmissile)
                player.life(1)
    for md_RRmissile in MD_Missile_L:
        if collide(md_RRmissile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_RRmissile)
                player.life(1)
    for md_Lmissile in MD_Missile_L:
        if collide(md_Lmissile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_Lmissile)
                player.life(1)
    for md_LLmissile in MD_Missile_L:
        if collide(md_LLmissile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_LLmissile)
                player.life(1)

    for b_Rmissile in B_Missile_L:
        if collide(b_Rmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_Rmissile)
                player.life(1)
    for b_RRmissile in B_Missile_L:
        if collide(b_RRmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_RRmissile)
                player.life(1)
    for b_RRRmissile in B_Missile_L:
        if collide(b_RRRmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_RRRmissile)
                player.life(1)
    for b_RRRRmissile in B_Missile_L:
        if collide(b_RRRRmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_RRRRmissile)
                player.life(1)
    for b_Lmissile in B_Missile_L:
        if collide(b_Lmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_Lmissile)
                player.life(1)
    for b_LLmissile in B_Missile_L:
        if collide(b_LLmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_LLmissile)
                player.life(1)
    for b_LLLmissile in B_Missile_L:
        if collide(b_LLLmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_LLLmissile)
                player.life(1)
    for b_LLLLmissile in B_Missile_L:
        if collide(b_LLLLmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_LLLLmissile)
                player.life(1)

def draw(frame_time):
    clear_canvas()
    map.draw()

    for enemyone in EnemyOne_L:
        enemyone.draw()
        enemyone.draw_bb()
    for enemytwo in EnemyTwo_L:
        enemytwo.draw()
        enemytwo.draw_bb()
    for enemythree in EnemyThree_L:
        enemythree.draw()
        enemythree.draw_bb()
    for enemyfour in EnemyFour_L:
        enemyfour.draw()
        enemyfour.draw_bb()
    for middleboss in MiddleBoss_L:
        middleboss.draw()
    for boss in Boss_L:
        boss.draw()

    player.draw()
    player.draw_bb()

    for missile1 in Missile1_L:
        missile1.draw()
        missile1.draw_bb()
    for missile2 in Missile2_L:
        missile2.draw()
        missile2.draw_bb()
    for missile3 in Missile3_L:
        missile3.draw()
        missile3.draw_bb()

    for e_missile in E_Missile_L:
        e_missile.draw()
        e_missile.draw_bb()
    for md_missile in MD_Missile_L:
        md_missile.draw()
        md_missile.draw_bb()
    for md_Rmissile in MD_Missile_L:
        md_Rmissile.draw()
        md_Rmissile.draw_bb()
    for md_RRmissile in MD_Missile_L:
        md_RRmissile.draw()
        md_RRmissile.draw_bb()
    for md_Lmissile in MD_Missile_L:
        md_Lmissile.draw()
        md_Lmissile.draw_bb()
    for md_LLmissile in MD_Missile_L:
        md_LLmissile.draw()
        md_LLmissile.draw_bb()
    for b_Rmissile in B_Missile_L:
        b_Rmissile.draw()
        b_Rmissile.draw_bb()
    for b_RRmissile in B_Missile_L:
        b_RRmissile.draw()
        b_RRmissile.draw_bb()
    for b_RRRmissile in B_Missile_L:
        b_RRRmissile.draw()
        b_RRRmissile.draw_bb()
    for b_RRRRmissile in B_Missile_L:
        b_RRRRmissile.draw()
        b_RRRRmissile.draw_bb()
    for b_Lmissile in B_Missile_L:
        b_Lmissile.draw()
        b_Lmissile.draw_bb()
    for b_LLmissile in B_Missile_L:
        b_LLmissile.draw()
        b_LLmissile.draw_bb()
    for b_LLLmissile in B_Missile_L:
        b_LLLmissile.draw()
        b_LLLmissile.draw_bb()
    for b_LLLLmissile in B_Missile_L:
        b_LLLLmissile.draw()
        b_LLLLmissile.draw_bb()

    for blast in Blast_L:
        blast.draw()

    ga1.draw()
    ga2.draw()

    update_canvas()


