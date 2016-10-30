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
        self.create_MiddleBoss()
        self.create_Boss()

    def create_EnemyOne(self):
        if (self.time_one >= 3 and self.boss_live == False):
            new_EnemyOne = EnemyOne()
            EnemyOne_L.append(new_EnemyOne)
            self.time_one = 0.0

    def create_MiddleBoss(self):
        if (self.middle_count >= 40 and self.boss_live == False):
            self.middle_live = True
            new_MiddleBoss = MiddleBoss()
            MiddleBoss_L.append(new_MiddleBoss)
            self.middle_count = 0.0

    def create_Boss(self):
        if (self.boss_count >= 80 and self.boss_live == False):
            self.boss_live = True
            new_Boss = Boss()
            Boss_L.append(new_Boss)
            self.boss_count = 0.0

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
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    DOWN_RUN, UP_RUN, DOWN_STAND, UP_STAND = 0, 1, 2, 3

    image = None

    def __init__(self):
        if EnemyOne.image == None:
            EnemyOne.image = load_image('object/Enemy/Enemy1.png')
        self.x, self.y = random.randint(100, 750), random.randint(1000, 1100)
        self.xdir = 0
        self.ydir = 0
        self.frame = random.randint(0, 4)
        self.run_frame = 0
        self.stand_frame = 0
        self.total_frames = 0.0
        self.state = self.DOWN_RUN
        self.name = 'enemyone'

    def handle_down_run(self):
        self.ydir = -1
        self.run_frame += 1
        if self.y < 150:
            self.state = self.UP_RUN
            self.y = 150
        if self.run_frame == 60:
            self.state = self.DOWN_STAND
            self.stand_frame = 0
    def handle_down_stand(self):
        self.stand_frame += 1
        if self.stand_frame == 60:
            self.state = self.DOWN_RUN
            self.run_frame = 0

    def handle_up_run(self):
        self.ydir = 1
        self.run_frame += 1
        if self.y  > 700:
            self.state = self.DOWN_RUN
            self.y = 700
        if self.run_frame == 60:
            self.state = self.UP_STAND
            self.stand_frame = 0
    def handle_up_stand(self):
        self.stand_frame += 1
        if self.stand_frame == 60:
            self.state = self.UP_RUN
            self.run_frame = 0

    handle_state = {
        DOWN_RUN: handle_down_run, UP_RUN: handle_up_run, DOWN_STAND: handle_down_stand, UP_STAND: handle_up_stand}

    def update(self,frame_time):
        distance = EnemyOne.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyOne.FRAMES_PER_ACTION * EnemyOne.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)

    def draw(self):
        self.image.clip_draw(self.frame * 160, 0, 160, 180, self.x, self.y)

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
        self.xdir = 0
        self.ydir = 0
        self.frame = random.randint(0,7)
        self.run_frame = 0
        self.stand_frame = 0
        self.total_frames = 0.0
        self.name = 'middleboss'
        self.state  =  self.DOWN_IDLE
        if MiddleBoss.image == None:
            MiddleBoss.image = load_image('object/Enemy/MiddleBoss.png')

    def handle_down_idle(self):
        self.ydir = -1
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
        self.x, self.y = 400, 1200
        self.xdir = 0
        self.ydir = 0
        self.frame = random.randint(0,7)
        self.run_frame = 0
        self.stand_frame = 0
        self.total_frames = 0.0
        self.state  =  self.DOWN_IDLE
        self.name = 'boss'
        if Boss.image == None:
            Boss.image = load_image('object/Enemy/Boss.png')

    def handle_down_idle(self):
        self.ydir= -1
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

    def get_missile1(self):
        newM1 = Missile1(self.x, self.y + 50)
        Missile1_L.append(newM1)

    def get_missile2(self):
        newM2 = Missile2(self.x, self.y + 50)
        Missile2_L.append(newM2)

    def get_missile3(self):
        newM3 = Missile3(self.x, self.y + 50)
        Missile3_L.append(newM3)


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
        self.ydir = 1

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_z:
            player.get_missile1()

    def update(self,frame_time):
        distance = Missile1.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

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
        self.ydir = 1

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_x:
            player.get_missile2()

    def update(self,frame_time):
        distance = Missile2.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

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
        self.ydir = 1

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_c:
            player.get_missile3()

    def update(self,frame_time):
        distance = Missile3.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

        if(self.y > 750) :
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

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 1

    image = None

    def __init__(self):
        self.x, self.y = 200, -200
        self.ydir = 0
        self.grandattack1 = 0
        if GrandAttack1.image == None:
            GrandAttack1.image = load_image('object/Player/GrateAttack1.png')

    def update(self,frame_time):
        distance = GrandAttack1.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

    def handle_events(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            self.grandattack1 = 1
            self.ydir = 1
            if self.grandattack1 == 1:
                if self.y > 1000:
                    self.grandattack1 = 0
                    self.y = -200

    def draw(self):
        self.image.draw(self.x, self.y)

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
        self.ydir = 0
        self.grandattack2 = 0
        if GrandAttack2.image == None:
            GrandAttack2.image = load_image('object/Player/GrateAttack2.png')

    def update(self,frame_time):
        distance = GrandAttack2.RUN_SPEED_PPS * frame_time
        self.y += (self.ydir * distance)

    def handle_events(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            self.grandattack2 = 1
            self.ydir = 1
            if self.grandattack2 == 1:
                if self.y > 1000:
                    self.grandattack2 = 0
                    self.y = -200

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
    global timer, map, player, ga1, ga2, EnemyOne_L, EnemyTwo_L, EnemyThree_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L, Missile3_L
    game_framework.reset_time()
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
    MiddleBoss_L = []
    Boss_L = []

def exit():
    global timer, map, player, ga1, ga2, EnemyOne_L, EnemyTwo_L, EnemyThree_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L, Missile3_L
    del(timer)
    del(player)
    del(Missile1_L)
    del(Missile2_L)
    del(Missile3_L)
    del(EnemyOne_L)
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
    for middleboss in MiddleBoss_L:
        middleboss.update(frame_time)
    for boss in Boss_L:
        boss.update(frame_time)

def draw(frame_time):
    clear_canvas()
    map.draw()

    for enemyone in EnemyOne_L:
        enemyone.draw()
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

    ga1.draw()
    ga2.draw()

    update_canvas()


# 현재 상태 : 게임 시작 됌, 적 1만 설정 완료