import random

import game_framework
import title_state
from pico2d import *

name = "MainState"

running = None
player = None
boss = None

Missile1_L = []
Missile2_L = []
Missile3_L = []
GrandAttack_L = []
EnemyOne_L = []
EnemyTwo_L = []
EnemyThree_L = []
MiddleBoss_L = []
Boss_L= []

class Timer:
    def __init__(self):
        self.time_one = 0.0
        self.time_two = 0.0
        self.time_three = 0.0
        self.middle_count = 0.0
        self.middle_live = False
        self.boss_count = 0.0
        self.boss_live = False

    def update(self, frame_time):
        self.time_one += frame_time
        self.time_two += frame_time
        self.time_three += frame_time
        self.middle_count += frame_time
        self.boss_count += frame_time
        self.create_EnemyOne()
        self.create_EnemyTwo()
        self.create_EnemyThree()
        self.create_MiddleBoss()
        self.create_Boss()

    def create_EnemyOne(self):
        if (self.time_one >= 3 and self.boss_live == False):
            new_EnemyOne = EnemyOne()
            EnemyOne_L.append(new_EnemyOne)
            self.time_one = 0.0

    def create_EnemyTwo(self):
        if (self.time_two >= 2 and self.boss_live == False):
            new_EnemyTwo = EnemyTwo()
            EnemyTwo_L.append(new_EnemyTwo)
            self.time_one = 0.0

    def create_EnemyThree(self):
        if (self.time_three >= 5 and self.boss_live == False):
            new_EnemyThree = EnemyThree()
            EnemyThree_L.append(new_EnemyThree)
            self.time_three = 0.0

    def create_MiddleBoss(self):
        if (self.Middle_count >= 40 and self.boss_live == False):
            self.Middle_live = True
            new_MiddleBoss = MiddleBoss()
            MiddleBoss_L.append(new_MiddleBoss)
            self.Middle_count = 0.0

    def create_Boss(self):
        if (self.Boss_count >= 80 and self.boss_live == False):
            self.Boss_live = True
            new_Boss = Boss()
            Boss_L.append(new_Boss)
            self.Boss_count = 0.0

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

class EnemyOne:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = None

    DOWNLEFT_RUN, DOWNRIGHT_RUN, DOWNLEFT_STAND, DOWNRIGHT_STAND = 0, 1, 2, 3

    def __init__(self):
        if EnemyOne.image == None:
            EnemyOne.image = load_image('object/Enemy/Enemy1.png')
        self.x, self.y = random.randint(80, 750), random.randint(1000, 1100)
        self.xdir = 0
        self.ydir = 0
        self.frame = 1
        self.run_frames = 0
        self.stand_fraems = 0
        self.total_frames = 0.0
        self.state = self.DOWNRIGHT_RUN
        self.name = 'enemyone'

    def handle_downleft_run(self):
        self.xdir = -1
        self.ydir = -1
        self.run_frames += 1
        if self.y < 400:
            self.state = self.DOWNLEFT_STAND
            self.y = 400
        if self.run_frames == random.randint(130,150):
            self.state = self.DOWNLEFT_RUN
            self.run_frames = 0

    def handle_downleft_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 50:
            self.state = self.DOWNLEFT_RUN
            self.run_frames = 0

    def handle_downright_run(self):
        self.xdir = 1
        self.ydir = -1
        self.run_frames += 1
        if self.y < 0:
            self.state = self.DOWNRIGHT_RUN
            self.y = random.randint(1000, 1100)
        if self.run_frames == random.randint(200, 250):
            self.state = self.DOWNRIGHT_STAND
            self.stand_frames = 0

    def handle_downright_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 50:
            self.state = self.DOWNRIGHT_RUN
            self.run_frames = 0

    handle_state = {
        DOWNLEFT_RUN: handle_downleft_run,
        DOWNRIGHT_RUN: handle_downright_run,
        DOWNLEFT_STAND: handle_downleft_stand,
        DOWNRIGHT_STAND: handle_downright_stand
    }

    def update(self,frame_time):
        distance = EnemyOne.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyOne.FRAMES_PER_ACTION * EnemyOne.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)
        self.x += (self.x * distance)
        self.y += (self.y * distance)
        self.handle_state[self.state](self)

    def draw(self):
        self.image.clip_draw(self.frame * 150, 150, 0, 165, self.x, self.y)

class EnemyTwo:
    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = None

    DOWNLEFT_RUN, DOWNRIGHT_RUN = 0, 1

    def __init__(self):
        if EnemyTwo.image == None:
            EnemyTwo.image = load_image('object/Enemy/Enemy2.png')
        self.x, self.y = random.randint(-100, 00), random.randint(500, 1100)
        self.xdir = 0
        self.ydir = 0
        self.frame = 1
        self.run_frames = 0
        self.total_frames = 0.0
        self.state = self.DOWNLEFT_RUN
        self.frame = 0
        self.name = 'enemytwo'

    def handle_downleft_run(self):
        self.xdir = -1
        self.ydir = -1
        self.run_frames += 1
        if self.y < 400:
            self.state = self.DOWNRIGHT_RUN
            self.ydir = +1
        if self.y < 200:
            self.state = self.DOWNLEFT_RUN
            self.ydir = -1
        if self.y < 0:
            self.state = self.DOWNRIGHT_RUN
            self.y = random.randint(1000, 1100)

    def handle_downright_run(self):
        self.xdir = 1
        self.ydir = -1
        self.run_frames += 1
        if self.y < 400:
            self.state = self.DOWNRIGHT_RUN
            self.ydir = +1
        if self.y < 200:
            self.state = self.DOWNLEFT_RUN
            self.ydir = -1

    handle_state = {
        DOWNLEFT_RUN: handle_downleft_run,
        DOWNRIGHT_RUN: handle_downright_run,
    }

    def update(self,frame_time):
        distance = EnemyTwo.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyTwo.FRAMES_PER_ACTION * EnemyTwo.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)

    def draw(self):
        self.image.clip_draw(self.frame * 56, 0, 56, 84, self.x, self.y)

class EnemyThree:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    DOWNLEFT_RUN, DOWNRIGHT_RUN = 0, 1

    image = None

    def __init__(self):
        if EnemyThree.image == None:
            EnemyThree.image = load_image('object/Enemy/Enemy3.png')
        self.x, self.y = random.randint(800, 1000), random.randint(500, 1100)
        self.frame = 1
        self.run_frames = 0
        self.total_frames = 0
        self.state = self.DOWNRIGHT_RUN
        self.name = 'enemythree'

    def handle_downleft_run(self):
        self.xdir = -1
        self.ydir = -1
        self.run_frames += 1
        if self.y < 400:
            self.state = self.DOWNRIGHT_RUN
            self.ydir = +1
        if self.y < 200:
            self.state = self.DOWNLEFT_RUN
            self.ydir = -1
        if self.y < 0:
            self.state = self.DOWNRIGHT_RUN
            self.y = random.randint(1000, 1100)

    def handle_downright_run(self):
        self.xdir = 1
        self.ydir = -1
        self.run_frames += 1
        if self.y < 500:
            self.state = self.DOWNRIGHT_RUN
            self.ydir = +1
        if self.y < 300:
            self.state = self.DOWNLEFT_RUN
            self.ydir = -1

    handle_state = {
        DOWNLEFT_RUN: handle_downleft_run,
        DOWNRIGHT_RUN: handle_downright_run,
    }

    def update(self,frame_time):
        distance = EnemyThree.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyThree.FRAMES_PER_ACTION * EnemyThree.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)

    def draw(self):
        self.image.clip_draw(self.frame * 120, 0, 120, 160, self.x, self.y)

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
        self.x, self.y = 200, 3000
        self.xdir = 0
        self.ydir = 0
        self.frame = random.randint(0,1)
        self.run_frame = 0
        self.stand_frame = 0
        self.total_frames = 0.0
        self.name = 'middleboss'
        self.state  =  self.DOWN_IDLE
        if MiddleBoss.image == None:
            MiddleBoss.image = load_image('object/Enemy/MiddleBoss.png')

    def handle_down_idle(self):
        self.ydif = -1
        if self.y < 580:
            self.ydir = 0
            self.state = self.DOWN_IDLE

    handle_state = {
            DOWN_IDLE: handle_down_idle
    }

    def update(self,frame_time):
        distance = MiddleBoss.RUN_SPEED_PPS * frame_time
        self.total_frames += MiddleBoss.FRAMES_PER_ACTION * MiddleBoss.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
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
        self.x, self.y = 600, 4000
        self.xdir = 0
        self.ydir = 0
        self.frame = random.randint(0,1)
        self.run_frame = 0
        self.stand_frame = 0
        self.total_frames = 0.0
        self.state  =  self.DOWN_IDLE
        self.name = 'boss'
        if Boss.image == None:
            Boss.image = load_image('object/Enemy/Boss.png')

    def handle_down_idle(self):
        self.ydif = -1
        if self.y < 580:
            self.ydir = 0
            self.state = self.DOWN_IDLE

    handle_state = {
            DOWN_IDLE: handle_down_idle
    }

    def update(self,frame_time):
        distance = Boss.RUN_SPEED_PPS * frame_time
        self.total_frames += Boss.FRAMES_PER_ACTION * Boss.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)

    def draw(self):
             self.image.clip_draw(self.frame * 420, 0, 420, 300, self.x, self.y)

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

        global rightmove, leftmove, upmove, downmove
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

        def draw(self):
            self.image.draw(self.x, self.y)

        def get_missile1(self):
            newM1 = Missile1(self.x, self.y + 50)
            Missile1_L.append(newM1)

        def get_missile2(self):
            newM2 = Missile2(self.x, self.y + 50)
            Missile1_L.append(newM2)

        def get_missile3(self):
            newM2 = Missile3(self.x, self.y + 50)
            Missile1_L.append(newM2)


class Missile1:
    PIXEL_PER_METER = (25.0 / 0.1)
    RUN_SPEED_KMPH = 30.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ydir = 1

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_z:
            player.get_missile1()

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

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_x:
            player.get_missile2()

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

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_x:
            player.get_missile2()

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

    image = None

    def __init__(self):
        self.x = 200
        self.y = -200
        self.ydir = 1
        self.initialization = 0
        if GrandAttack1.image == None:
            GrandAttack1.image = load_image('object/Player/GrateAttack1.png')

    def update(self,frame_time):
        self.initialization = 1
        distance = GrandAttack1.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

        if self.initialization == 1:
            if GrandAttack1.y > 750:
                self.initialization = 0

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            if self.initialization == 0:
                self.initialization = 1
                self.ydir = 1

    def draw(self):
        self.image.draw(self.x, self.y)

class GrandAttack2:
    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self):
        self.x = -200
        self.y = -200
        self.ydir = 1
        self.initialization = 0
        if GrandAttack2.image == None:
            GrandAttack2.image = load_image('object/Player/GrateAttack2.png')

    def update(self,frame_time):
        self.initialization = 1
        distance = GrandAttack2.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

        if self.initialization == 1:
            if GrandAttack1.y > 750:
                self.initialization = 0

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            if self.initialization == 0:
                self.initialization = 1
                self.ydir = 1

    def draw(self):
        self.image.draw(self.x, self.y)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        else:
            player.handle_event(event)
            ga1.handle_event(event)
            ga2.handle_event(event)
            missile1.handle_events(event)
            missile2.handle_events(event)
            missile3.handle_events(event)

def enter():
    global timer, map, player, enemyone, enemytwo, enemythree, middleboss, boss, ga1, ga2, EnemyOne_L,\
        EnemyTwo_L, EnemyThree_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L, Missile3_L

    map = Map(800, 750)

    timer = Timer()
    player = Player()

    missile1 = Missile1(0,0)
    missile2 = Missile2(0,0)
    missile3 = Missile3(0,0)

    ga1 = GrandAttack1()
    ga2 = GrandAttack2()

    Missile1_L = []
    Missile2_L = []
    Missile3_L = []
    EnemyOne_L = []
    EnemyTwo_L = []
    EnemyThree_L = []
    MiddleBoss_L = []
    Boss_L = []

def exit():
    global timer, map, player, enemyone, enemytwo, enemythree, middleboss, boss, ga1, ga2, EnemyOne_L, \
        EnemyTwo_L, EnemyThree_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L, Missile3_L
    del(timer)
    del(player)
    del(Missile1_L)
    del(Missile2_L)
    del(Missile3_L)
    del(EnemyOne_L)
    del(EnemyTwo_L)
    del(EnemyThree_L)
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
    timer.update(frame_time)
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

    for enemyone in EnemyOne_L:
        enemyone.update(frame_time)
    for enemytwo in EnemyTwo_L:
        enemytwo.update(frame_time)
    for enemythree in EnemyThree_L:
        enemythree.update(frame_time)
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

    player.draw()

    for missile1 in Missile1_L:
        missile1.draw()
    for missile2 in Missile2_L:
        missile2.draw()
    for missile3 in Missile3_L:
        missile3.draw()

    ga1.draw()
    ga2.draw()

    update_canvas()




