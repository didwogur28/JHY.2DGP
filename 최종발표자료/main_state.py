import random
import os

import game_framework
import start_state
import title_state
import exit_state


from Map import Map
from Missile import GrandAttack1
from Missile import GrandAttack2
from Blast import Blast1
from Blast import Blast2
from Blast import Blast3

from pico2d import *

name = "MainState"

running = None
player = None


Missile1_L = []
Missile2_L = []
Missile3_L = []
E_Missile_L = []
MD_Missile_L = []
B_Missile_L = []
Blast1_L = []
Blast2_L = []
Item_HP_L = []
Item_GA_L = []

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
    attacksound = None
    GetItemsound = None

    LEFT_RUN, RIGHT_RUN, IDLE, UP_RUN, DOWN_RUN = 0, 1, 2, 3, 4

    def __init__(self):
        self.x = 400
        self.y = 100
        self.xx = 0
        self.yy = 0
        self.HEART = 1
        self.gage = 10
        self.state = self.IDLE
        self.frame = 0
        self.total_frames = 0.0
        self.life_time = 0.0
        if Player.image == None:
            Player.image = load_image('object/Player/Player.png')
        if Player.attacksound == None:
            Player.attacksound = load_wav('object\\Sound\\Enemybombsound.wav')
            Player.attacksound.set_volume(8)
        if self.GetItemsound == None:
            self.GetItemsound = load_wav('object\\Sound\\Getitem.wav')
            self.GetItemsound.set_volume(20)

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

    def attacks(self):
        self.attacksound.play()

    def getitems(self,item_hp):
        self.GetItemsound.play()

    def getitemss(self, item_ga):
        self.GetItemsound.play()

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

    def get_bb(self):
        return self.x -30, self.y -50, self.x+30, self.y+30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def life(self, life_down):
        self.gage -= life_down
        if(self.gage <= 0):
            self.HEART = 0
            return self.HEART
        else:
            return self.HEART

class HP:
    def __init__(self):
        self.x = 165
        self.y = 700

    def update(self,frame_time):
        if player.gage == 10:
            self.image = load_image('object/Hp/Hp10.png')
        if player.gage == 9:
            self.image = load_image('object/Hp/Hp9.png')
        if player.gage == 8:
            self.image = load_image('object/Hp/Hp8.png')
        if player.gage == 7:
            self.image = load_image('object/Hp/Hp7.png')
        if player.gage == 6:
            self.image = load_image('object/Hp/Hp6.png')
        if player.gage == 5:
            self.image = load_image('object/Hp/Hp5.png')
        if player.gage == 4:
            self.image = load_image('object/Hp/Hp4.png')
        if player.gage == 3:
            self.image = load_image('object/Hp/Hp3.png')
        if player.gage == 2:
            self.image = load_image('object/Hp/Hp2.png')
        if player.gage == 1:
            self.image = load_image('object/Hp/Hp1.png')
        if player.gage == 0:
            self.image = load_image('object/Hp/Hp0.png')

    def draw(self):
        self.image.draw(self.x, self.y)

class HPBAR:
    def __init__(self):
        self.x = 40
        self.y = 703
        self.image = load_image('object/Hp/HPBAR.png')

    def draw(self):
        self.image.draw(self.x, self.y)

class GA_UI:
    def __init__(self):
        self.x = 130
        self.y = 50

    def update(self, frame_time):
        if ga1.countga1 == 3:
            self.image = load_image('object/GA_UI/GA_ui3.png')
        if ga1.countga1 == 2:
            self.image = load_image('object/GA_UI/GA_ui2.png')
        if ga1.countga1 == 1:
            self.image = load_image('object/GA_UI/GA_ui1.png')
        if ga1.countga1 == 0:
            self.image = load_image('object/GA_UI/GA_ui0.png')

    def draw(self):
        self.image.draw(self.x, self.y)

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
        self.gage = 220
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
        self.gage = 80
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
        self.gage = 210
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
        self.gage = 80
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
        self.HEART = True
        self.gage = 5000
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
            md_missile2 = MD_Missile(self.x , self.y - 120)
            md_missile3 = MD_Missile(self.x , self.y - 210)
            md_missile4 = MD_RMissile(self.x + 40, self.y - 30)
            md_missile5 = MD_RMissile(self.x + 60, self.y - 120)
            md_missile6 = MD_RMissile(self.x + 80, self.y - 210)
            md_missile7 = MD_RRMissile(self.x + 20, self.y - 30)
            md_missile8 = MD_RRMissile(self.x + 30, self.y - 120)
            md_missile9 = MD_RRMissile(self.x + 40, self.y - 210)
            md_missile10 = MD_LMissile(self.x - 40, self.y - 30)
            md_missile11 = MD_LMissile(self.x - 60, self.y - 120)
            md_missile12 = MD_LMissile(self.x - 80, self.y - 210)
            md_missile13 = MD_LLMissile(self.x - 20, self.y - 30)
            md_missile14 = MD_LLMissile(self.x - 30, self.y - 120)
            md_missile15 = MD_LLMissile(self.x - 40, self.y - 210)

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

    def draw(self):
             self.image.clip_draw(self.frame * 320, 0, 320, 390, self.x, self.y)

    def get_bb(self):
        return self.x - 130, self.y -160, self.x + 150, self.y + 150

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def life(self, life_down):
        self.gage -= life_down
        if(self.gage <= 0):
            self.HEART  = False
            return self.HEART
        else:
            return self.HEART


class Boss:
    PIXEL_PER_METER = (10.0 / 0.5)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    E_Missile_Time = 3

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
        self.missile_c1 = 0
        self.missile_c2 = 0
        self.missile_c3 = 0
        self.missile_c4 = 0
        self.missile_c5 = 0
        self.missile_c6 = 0
        self.missile_c7 = 0
        self.missile_c8 = 0
        self.HEART = True
        self.gage = 8000
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
        if self.y < 600:
            self.missile_c1 += frame_time * self.E_Missile_Time
            self.missile_c2 += frame_time * self.E_Missile_Time
            self.missile_c3 += frame_time * self.E_Missile_Time
            self.missile_c4 += frame_time * self.E_Missile_Time
            self.missile_c5 += frame_time * self.E_Missile_Time
            self.missile_c6 += frame_time * self.E_Missile_Time
            self.missile_c7 += frame_time * self.E_Missile_Time
            self.missile_c8 += frame_time * self.E_Missile_Time

        if self.missile_c1 > 1:
            self.missile_c1 = -11
            b_missile1 = B_Missile(self.x, self.y)
            B_Missile_L.append(b_missile1)
        if self.missile_c2 > 1.5:
            self.missile_c2 = -10.5
            b_missile2 = B_DMissile(self.x - 40, self.y)
            b_missile3 = B_DMissile(self.x + 40, self.y)
            B_Missile_L.append(b_missile2), B_Missile_L.append(b_missile3)
        if self.missile_c3 > 2:
            self.missile_c3 = -10
            b_missile4 = B_DOMissile(self.x - 80, self.y)
            b_missile5 = B_DOMissile(self.x, self.y)
            b_missile6 = B_DOMissile(self.x + 80, self.y)
            B_Missile_L.append(b_missile4), B_Missile_L.append(b_missile5), B_Missile_L.append(b_missile6)
        if self.missile_c4 > 2.5:
            self.missile_c4 = -9.5
            b_missile7 = B_DOWMissile(self.x - 120, self.y)
            b_missile8 = B_DOWMissile(self.x - 40, self.y)
            b_missile9 = B_DOWMissile(self.x + 40, self.y)
            b_missile10 = B_DOWMissile(self.x + 120, self.y)
            B_Missile_L.append(b_missile7), B_Missile_L.append(b_missile8), B_Missile_L.append(b_missile9), B_Missile_L.append(b_missile10)
        if self.missile_c5 > 3:
            self.missile_c5 = -9
            b_missile11 = B_DOWNMissile(self.x - 160, self.y)
            b_missile12 = B_DOWNMissile(self.x - 80, self.y)

            b_missile13 = B_DOWNMissile(self.x - 0, self.y)
            b_missile14 = B_DOWNMissile(self.x + 80, self.y)
            b_missile15 = B_DOWNMissile(self.x + 160, self.y)
            B_Missile_L.append(b_missile11), B_Missile_L.append(b_missile12), B_Missile_L.append(
                b_missile13), B_Missile_L.append(b_missile14), B_Missile_L.append(b_missile15)

        if self.missile_c6 > 4.5:
            self.missile_c6 = -7.5
            b_missile16 = B_CMissile(self.x, self.y)
            b_missile17 = B_RMissile(self.x + 40, self.y)
            b_missile18 = B_RRMissile(self.x + 20, self.y)
            b_missile19 = B_LMissile(self.x - 20, self.y)
            b_missile20 = B_LLMissile(self.x - 40, self.y)
            B_Missile_L.append(b_missile16), B_Missile_L.append(b_missile17), B_Missile_L.append(
                b_missile18), B_Missile_L.append(b_missile19), B_Missile_L.append(b_missile20)
        if self.missile_c7 > 5:
            self.missile_c7 = -7
            b_missile21 = B_CMissile(self.x , self.y)
            b_missile22 = B_RMissile(self.x + 60, self.y)
            b_missile23 = B_RRMissile(self.x + 30, self.y)
            b_missile24 = B_LMissile(self.x - 60, self.y)
            b_missile25 = B_LLMissile(self.x - 30, self.y)
            B_Missile_L.append(b_missile21), B_Missile_L.append(b_missile22), B_Missile_L.append(
                b_missile23), B_Missile_L.append(b_missile24), B_Missile_L.append(b_missile25)
        if self.missile_c8 > 5.5:
            self.missile_c8 = -6.5
            b_missile26 = B_CMissile(self.x , self.y)
            b_missile27 = B_RMissile(self.x + 80, self.y)
            b_missile28 = B_RRMissile(self.x + 40, self.y)
            b_missile29 = B_LMissile(self.x - 80, self.y)
            b_missile30 = B_LLMissile(self.x - 40, self.y)
            B_Missile_L.append(b_missile26), B_Missile_L.append(b_missile27), B_Missile_L.append(
                b_missile28), B_Missile_L.append(b_missile29), B_Missile_L.append(b_missile30)

    def draw(self):
             self.image.clip_draw(self.frame * 420, 0, 420, 300, self.x, self.y)

    def get_bb(self):
        return self.x - 180, self.y -250, self.x + 200, self.y + 250

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def life(self, life_down):
        self.gage -= life_down
        if(self.gage <= 0):
            self.HEART  = False
            return self.HEART
        else:
            return self.HEART

class Create:
    def __init__(self):
        self.create1 = 0.0
        self.create2 = 0.0
        self.create3 = 0.0
        self.create4 = 0.0
        self.createitem_hp = 0.0
        self.createitem_ga = 0.0
        self.createmiddle = 0.0
        self.createboss = 0.0
        self.middlel = False
        self.bossl = False

    def update(self, frame_time):
        self.create1 += frame_time
        self.create2 += frame_time
        self.create3 += frame_time
        self.create4 += frame_time
        self.createitem_hp += frame_time
        self.createitem_ga += frame_time
        self.createmiddle += frame_time
        self.createboss += frame_time
        self.CEnemyOne()
        self.CEnemyTwo()
        self.CEnemyThree()
        self.CEnemyFour()
        self.CMiddleBoss()
        self.CBoss()
        self.CItem_HP()
        self.CItem_GA()

    def CEnemyOne(self):
        if self.create1 >= 3:
            nEnemyOne = EnemyOne()
            EnemyOne_L.append(nEnemyOne)
            self.create1 = 0.0
            if self.bossl == True:
                if self.create1 >= 10:
                    EnemyOne_L.append(nEnemyOne)

    def CEnemyTwo(self):
        if self.create2 >= 2:
            nEnemyTwo = EnemyTwo()
            EnemyTwo_L.append(nEnemyTwo)
            self.create2 = 0.0
            if self.bossl == True:
                if self.create2 >= 15:
                    EnemyTwo_L.append(nEnemyTwo)

    def CEnemyThree(self):
        if self.create3 >= 5:
            nEnemyThree = EnemyThree()
            EnemyThree_L.append(nEnemyThree)
            self.create3 = 0.0
            if self.bossl == True:
                if self.create3 >= 18:
                    EnemyThree_L.append(nEnemyThree)

    def CEnemyFour(self):
        if self.create4 >= 2:
            nEnemyFour = EnemyFour()
            EnemyFour_L.append(nEnemyFour)
            self.create4 = 0.0
            if self.bossl == True:
                if self.create4 >= 15:
                    EnemyFour_L.append(nEnemyFour)

    def CMiddleBoss(self):
        if self.createmiddle >=30:
            self.middlel = True
            nMiddleBoss = MiddleBoss()
            MiddleBoss_L.append(nMiddleBoss)
            self.createmiddle = -100
        if self.bossl == True:
            self.middlel = False

    def CBoss(self):
        if (self.createboss >= 5):
            self.bossl = True
            nBoss = Boss()
            Boss_L.append(nBoss)
            if self.bossl == True:
                map.Bgm.pause()
                map.bosssound = load_music('object/Sound/bosssound.mp3')
                map.bosssound.set_volume(30)
                map.bosssound.repeat_play()
            self.createboss = -100

    def CItem_HP(self):
        if self.createitem_hp >= 5:
            nItem_hp = Item_HP()
            Item_HP_L.append(nItem_hp)
            self.createitem_hp = 0.0

    def CItem_GA(self):
        if self.createitem_ga >= 15:
            nItem_ga = Item_GA()
            Item_GA_L.append(nItem_ga)
            self.createitem_ga = 0.0

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
    PIXEL_PER_METER = (20.0 / 1.0)
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
            MD_Missile.image = load_image('object/Missile/MD_Missile.png')

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
    PIXEL_PER_METER = (20.0 / 1.0)
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
            MD_RMissile.image = load_image('object/Missile/MD_Missile.png')

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
    PIXEL_PER_METER = (20.0 / 1.0)
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
            MD_RRMissile.image = load_image('object/Missile/MD_Missile.png')

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
    PIXEL_PER_METER = (20.0 / 1.0)
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
            MD_LMissile.image = load_image('object/Missile/MD_Missile.png')

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
    PIXEL_PER_METER = (20.0 / 1.0)
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
            MD_LLMissile.image = load_image('object/Missile/MD_Missile.png')

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

class B_Missile:
    PIXEL_PER_METER = (20.0 / 1.0)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yy = -0.5

        if B_Missile.image == None:
            B_Missile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_Missile.RUN_SPEED_PPS * frame_time
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

class B_DMissile:
    PIXEL_PEL_METEL = (20.0 / 1.0)
    LUN_SPEED_KMPH = 10.0
    LUN_SPEED_MPM = (LUN_SPEED_KMPH * 1000.0 / 60.0)
    LUN_SPEED_MPS = (LUN_SPEED_MPM / 60.0)
    LUN_SPEED_PPS = (LUN_SPEED_MPS * PIXEL_PEL_METEL)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yy = -0.5

        if B_DMissile.image == None:
            B_DMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_DMissile.LUN_SPEED_PPS * frame_time
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

class B_DOMissile:
    PIXEL_PER_METER = (20.0 / 1.0)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yy = -0.5

        if B_DOMissile.image == None:
            B_DOMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_DOMissile.RUN_SPEED_PPS * frame_time
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

class B_DOWMissile:
    PIXEL_PER_METER = (20.0 / 1.0)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yy = -0.5

        if B_DOWMissile.image == None:
            B_DOWMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_DOWMissile.RUN_SPEED_PPS * frame_time
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

class B_DOWNMissile:
    PIXEL_PER_METER = (20.0 / 1.0)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yy = -0.5

        if B_DOWNMissile.image == None:
            B_DOWNMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_DOWNMissile.RUN_SPEED_PPS * frame_time
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

class B_CMissile:
    PIXEL_PER_METER = (20.0 / 1.0)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yy = -0.5
        if B_CMissile.image == None:
            B_CMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_CMissile.RUN_SPEED_PPS * frame_time
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
    PIXEL_PER_METER = (20.0 / 1.0)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = 0.5
        self.yy = -0.5

        if B_RMissile.image == None:
            B_RMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_RMissile.RUN_SPEED_PPS * frame_time
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

class B_RRMissile:
    PIXEL_PER_METER = (20.0 / 1.0)
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

        if B_RRMissile.image == None:
            B_RRMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_RRMissile.RUN_SPEED_PPS * frame_time
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

class B_LMissile:
    PIXEL_PER_METER = (20.0 / 1.0)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = -0.5
        self.yy = -0.5
        if B_LMissile.image == None:
            B_LMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_LMissile.RUN_SPEED_PPS * frame_time
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

class B_LLMissile:
    PIXEL_PER_METER = (20.0 / 1.0)
    RUN_SPEED_KMPH = 10.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xx = -0.25
        self.yy = -0.5
        if B_LLMissile.image == None:
            B_LLMissile.image = load_image('object/Missile/B_Missile.png')

    def update(self, frame_time):
        distance = B_LLMissile.RUN_SPEED_PPS * frame_time
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

class Missile1:
    PIXEL_PER_METER = (25.0 / 0.1)
    RUN_SPEED_KMPH = 30.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    missilesound = None

    def __init__(self, x, y):
        if Missile1.image == None:
            self.image = load_image('object/Missile/Missile1.png')
        self.x = x
        self.y = y
        self.yy = 1
        if Missile1.missilesound == None:
            Missile1.missilesound = load_wav('object/Sound/Missilesound.wav')
            Missile1.missilesound.set_volume(20)

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_z:
            player.get_missile1()
            self.missiles()

    def update(self,frame_time):
        distance = Missile1.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if(self.y > 750) :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def missiles(self):
        self.missilesound.play()

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
    missilesound = None

    def __init__(self, x, y):
        if Missile2.image == None:
            self.image = load_image('object/Missile/Missile2.png')
        self.x = x
        self.y = y
        self.yy = 1
        if Missile2.missilesound == None:
            Missile2.missilesound = load_wav('object/Sound/Missilesound.wav')
            Missile2.missilesound.set_volume(20)

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_x:
            player.get_missile2()
            self.missiles()

    def update(self,frame_time):
        distance = Missile2.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if(self.y > 750) :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def missiles(self):
        self.missilesound.play()

    def get_bb(self):
        return self.x - 10, self.y -15, self.x + 10, self.y + 15

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Item_HP:
    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    GetItemsound = None

    def __init__(self):
        if Item_HP.image == None:
            self.image = load_image('object/Item/Item_HP.png')
        self.x = random.randint(0, 800)
        self.y = 1000
        self.yy = -0.25

    def update(self, frame_time):
        distance = Item_HP.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if (self.y < 0):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 24, self.y -10, self.x + 24, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Item_GA:
    PIXEL_PER_METER = (25.0 / 0.5)
    RUN_SPEED_KMPH = 50.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    GetItemsound = None

    def __init__(self):
        if Item_GA.image == None:
            self.image = load_image('object/Item/Item_GA.png')
        self.x = random.randint(0, 800)
        self.y = 1000
        self.yy = -0.25

    def update(self, frame_time):
        distance = Item_HP.RUN_SPEED_PPS * frame_time
        self.y += (self.yy * distance)

        if (self.y < 0):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 24, self.y -10, self.x + 24, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True

class Ui:
    def __init__(self):
        self.font1 = load_font('object/Font/ENCR10B.TTF', 30)
        self.score = 0

    def draw(self):
        self.font1.draw(550, 700, 'Score: %d' % (self.score))
        if (player.HEART == 0):
            self.font2 = load_font('object/Font/HoonMakdaeyunpilR.TTF', 60)
            self.font2.draw(70, 400, 'ReStart : [1]   /   EXIT : [ESC]', (255,255,255))

    def sp(self, sp_in):
        self.score += sp_in

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            player.gage = 10
            player.HEART = True
            ga1.countga1 = 3
            ga2.countga2 = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_0:
            player.gage = 10000
        else:
            if player.HEART == True:
                player.handle_event(event)
                ga1.handle_events(event)
                ga2.handle_events(event)
                missile1.handle_events(event)
                missile2.handle_events(event)

def enter():
    global create, map, ui, player, hp,  hpbar, ga_ui, Item_HP_L, Item_GA_L, ga1, ga2, EnemyOne_L, EnemyTwo_L, EnemyThree_L, EnemyFour_L, E_Missile_L, MD_Missile_L, B_Missile_L, MiddleBoss_L, Boss_L, missile1, missile2, missile3, Missile1_L, Missile2_L,Blast1_L, Blast2_L, Blast3_L
    game_framework.reset_time()
    map = Map(800, 750)

    ui = Ui()
    create = Create()
    player = Player()
    hp = HP()
    hpbar = HPBAR()
    ga_ui = GA_UI()

    missile1 = Missile1(0,0)
    missile2 = Missile2(0,0)

    ga1 = GrandAttack1()
    ga2 = GrandAttack2()

    Missile1_L = []
    Missile2_L = []
    E_Missile_L = []
    MD_Missile_L = []
    B_Missile_L = []
    EnemyOne_L = []
    EnemyTwo_L = []
    EnemyThree_L = []
    EnemyFour_L = []
    MiddleBoss_L = []
    Boss_L = []
    Blast1_L = []
    Blast2_L = []
    Blast3_L = []
    Item_HP_L = []
    Item_GA_L = []

def exit():
    global create, map, ui, player, hp, hpbar, ga_ui,ga1, ga2, Item_HP_L, Item_GA_L, EnemyOne_L,EnemyTwo_L, EnemyThree_L, EnemyFour_L, E_Missile_L, MD_Missile_L, B_Missile_L, MiddleBoss_L, Boss_L, missile1, missile2,  Missile1_L, Missile2_L,  Blast1_L, Blast2_L, Blast3_L
    del(create)
    del(ui)
    del(player)
    del(hp)
    del(hpbar)
    del(ga_ui)
    del(Missile1_L)
    del(Missile2_L)
    del(EnemyOne_L)
    del(EnemyTwo_L)
    del(EnemyThree_L)
    del(EnemyFour_L)
    del(E_Missile_L)
    del(MD_Missile_L)
    del(MiddleBoss_L)
    del(Boss_L)
    del(Blast1_L)
    del(Blast2_L)
    del(Blast3_L)
    del(Item_HP_L)
    del(Item_GA_L)
    del(ga1)
    del(ga2)
    del(missile1)
    del(missile2)
    del(map)

    close_canvas()

def update(frame_time):
    create.update(frame_time)
    map.update(frame_time)
    hp.update(frame_time)
    ga_ui.update((frame_time))
    if (player.HEART == 1):
        player.update(frame_time)

    ga1.update(frame_time)
    ga2.update(frame_time)

    for blast1 in Blast1_L:
        blast1.update(frame_time)
        finish_blast1 = blast1.update(frame_time)
        if finish_blast1 == True:
            Blast1_L.remove(blast1)
    for blast2 in Blast2_L:
        blast2.update(frame_time)
        finish_blast2 = blast2.update(frame_time)
        if finish_blast2 == True:
            Blast2_L.remove(blast2)
    for blast3 in Blast3_L:
        blast3.update(frame_time)
        finish_blast3 = blast3.update(frame_time)
        if finish_blast3 == True:
            Blast3_L.remove(blast3)

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

    for b_missile in B_Missile_L:
        b_missile.update(frame_time)
        out = b_missile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_missile)
    for b_Dmissile in B_Missile_L:
        b_Dmissile.update(frame_time)
        out = b_Dmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_Dmissile)
    for b_DOmissile in B_Missile_L:
        b_DOmissile.update(frame_time)
        out = b_DOmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_DOmissile)
    for b_DOWmissile in B_Missile_L:
        b_DOWmissile.update(frame_time)
        out = b_DOWmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_DOWmissile)
    for b_DOWNmissile in B_Missile_L:
        b_DOWNmissile.update(frame_time)
        out = b_DOWNmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_DOWNmissile)
    for b_Cmissile in B_Missile_L:
        b_Cmissile.update(frame_time)
        out = b_Cmissile.update(frame_time)
        if out == True:
            B_Missile_L.remove(b_Cmissile)
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

    for item_hp in Item_HP_L:
        item_hp.update(frame_time)
    for item_ga in Item_GA_L:
        item_ga.update(frame_time)

# 충돌체크(플레이어, 적1,2,3,4) #
    for enemyone in EnemyOne_L:
        if collide(enemyone, player):
            if (player.HEART == 1):
                EnemyOne_L.remove(enemyone)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60
    for enemytwo in EnemyTwo_L:
        if collide(enemytwo, player):
            if (player.HEART == 1):
                EnemyTwo_L.remove(enemytwo)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60
    for enemythree in EnemyThree_L:
        if collide(enemythree, player):
            if (player.HEART == 1):
                EnemyThree_L.remove(enemythree)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60
    for enemyfour in EnemyFour_L:
        if collide(enemyfour, player):
            if (player.HEART == 1):
                EnemyFour_L.remove(enemyfour)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60
    for middleboss in MiddleBoss_L:
        if collide(middleboss, player):
            if (player.HEART == 1):
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60
    for boss in Boss_L:
        if collide(boss, player):
            if (player.HEART == 1):
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

# 충돌체크(플레이어 HP아이템)
    for item_hp in Item_HP_L:
        if collide(item_hp, player):
            if (player.gage == 10):
                player.getitems(item_hp)
                Item_HP_L.remove(item_hp)
            else:
                player.gage += 1
                player.getitems(item_hp)
                Item_HP_L.remove(item_hp)
# 충돌체크 (플레이어 GA아이템)
    for item_ga in Item_GA_L:
        if collide(item_ga, player):
            if ga1.countga1 == 3:
                player.getitemss(item_ga)
                Item_GA_L.remove(item_ga)
            else:
                ga1.countga1 += 1
                ga2.countga2 += 1
                player.getitemss(item_ga)
                Item_GA_L.remove(item_ga)

            # 충돌체크(플레이어 미사일, 적1,2,3,4) #
    for missile1 in Missile1_L:
        for enemyone in EnemyOne_L:
            if collide(missile1, enemyone):
                enemyone.life(120)
                Missile1_L.remove(missile1)
                enemyone_blast3 = Blast3(missile1.x, enemyone.y)
                Blast3_L.append(enemyone_blast3)
                ui.sp(7)
                if (enemyone.HEART == False):
                    EnemyOne_L.remove(enemyone)
                    enemyone_blast1 = Blast1(enemyone.x, enemyone.y)
                    Blast1_L.append(enemyone_blast1)
    for missile1 in Missile1_L:
        for enemytwo in EnemyTwo_L:
            if collide(missile1, enemytwo):
                enemytwo.life(100)
                Missile1_L.remove(missile1)
                enemytwo_blast3 = Blast3(missile1.x, enemytwo.y)
                Blast3_L.append(enemytwo_blast3)
                ui.sp(3)
                if (enemytwo.HEART == False):
                    EnemyTwo_L.remove(enemytwo)
                    enemytwo_blast1 = Blast1(enemytwo.x, enemytwo.y)
                    Blast1_L.append(enemytwo_blast1)
    for missile1 in Missile1_L:
        for enemythree in EnemyThree_L:
            if collide(missile1, enemythree):
                enemythree.life(100)
                Missile1_L.remove(missile1)
                enemythree_blast3 = Blast3(missile1.x, enemythree.y)
                Blast3_L.append(enemythree_blast3)
                ui.sp(5)
                if (enemythree.HEART == False):
                    EnemyThree_L.remove(enemythree)
                    enemythree_blast1 = Blast1(enemythree.x, enemythree.y)
                    Blast1_L.append(enemythree_blast1)
    for missile1 in Missile1_L:
        for enemyfour in EnemyFour_L:
            if collide(missile1, enemyfour):
                enemyfour.life(100)
                Missile1_L.remove(missile1)
                enemyfour_blast3 = Blast3(missile1.x, enemyfour.y)
                Blast3_L.append(enemyfour_blast3)
                ui.sp(3)
                if (enemyfour.HEART == False):
                    EnemyFour_L.remove(enemyfour)
                    enemyfour_blast1 = Blast1(enemyfour.x, enemyfour.y)
                    Blast1_L.append(enemyfour_blast1)

# 충돌체크(플레이어미사일, 중간보스,최종보스) #
    for missile1 in Missile1_L:
        for middleboss in MiddleBoss_L:
            if collide(missile1, middleboss):
                Missile1_L.remove(missile1)
                middleboss.life(100)
                middleboss_blast1 = Blast1(missile1.x, middleboss.y)
                Blast1_L.append(middleboss_blast1)
                ui.sp(10)
                if (middleboss.HEART == False):
                    MiddleBoss_L.remove(middleboss)
                    middlebossup_blast2 = Blast2(middleboss.x, middleboss.y + 100)
                    middlebossdown_blast2 = Blast2(middleboss.x, middleboss.y - 100)
                    Blast2_L.append(middlebossup_blast2)
                    Blast2_L.append(middlebossdown_blast2)

    for missile1 in Missile1_L:
        for boss in Boss_L:
            if collide(missile1, boss):
                Missile1_L.remove(missile1)
                boss.life(150)
                boss_blast1 = Blast1(missile1.x, boss.y)
                Blast1_L.append(boss_blast1)
                ui.sp(20)
                if (boss.HEART == False):
                    Boss_L.remove(boss)
                    create.bossl = False
                    bossup_blast2 = Blast2(boss.x, boss.y + 100)
                    bossdown_blast2 = Blast2(boss.x, boss.y - 100)
                    Blast2_L.append(bossup_blast2)
                    Blast2_L.append(bossdown_blast2)
                    if (boss.gage < 0):
                        create.create1 = -100
                        create.create2 = -100
                        create.create3 = -100
                        create.create4 = -100
                        create.createitem_hp = -100
                        create.createitem_ga = -100
                        for enemyone in EnemyOne_L:
                            EnemyOne_L.remove(enemyone)
                            enemyone_blast1 = Blast1(enemyone.x, enemyone.y)
                            Blast1_L.append(enemyone_blast1)
                        for enemytwo in EnemyTwo_L:
                            EnemyTwo_L.remove(enemytwo)
                            enemytwo_blast1 = Blast1(enemytwo.x, enemytwo.y)
                            Blast1_L.append(enemytwo_blast1)
                        for enemythree in EnemyThree_L:
                            EnemyThree_L.remove(enemythree)
                            enemythree_blast1 = Blast1(enemythree.x, enemythree.y)
                            Blast1_L.append(enemythree_blast1)
                        for enemyfour in EnemyFour_L:
                            EnemyFour_L.remove(enemyfour)
                            enemyfour_blast1 = Blast1(enemyfour.x, enemyfour.y)
                            Blast1_L.append(enemyfour_blast1)

    for missile2 in Missile2_L:
        for middleboss in MiddleBoss_L:
            if collide(missile2, middleboss):
                Missile2_L.remove(missile2)
                middleboss.life(150)
                middleboss_blast1 = Blast1(missile2.x, middleboss.y)
                Blast1_L.append(middleboss_blast1)
                ui.sp(10)
                if (middleboss.HEART == False):
                    MiddleBoss_L.remove(middleboss)
                    middlebossup_blast2 = Blast2(middleboss.x, middleboss.y + 100)
                    middlebossdown_blast2 = Blast1(middleboss.x, middleboss.y - 100)
                    Blast2_L.append(middlebossup_blast2)
                    Blast2_L.append(middlebossdown_blast2)
    for missile2 in Missile2_L:
        for boss in Boss_L:
            if collide(missile2, boss):
                Missile2_L.remove(missile2)
                boss.life(100)
                boss_blast1 = Blast1(missile2.x, boss.y)
                Blast1_L.append(boss_blast1)
                ui.sp(20)
                if (boss.HEART == False):
                    Boss_L.remove(boss)
                    create.bossl = False
                    bossup_blast2 = Blast2(boss.x, boss.y + 100)
                    bossdown_blast2 = Blast2(boss.x, boss.y - 100)
                    Blast2_L.append(bossup_blast2)
                    Blast2_L.append(bossdown_blast2)
                    if (boss.gage < 0):
                        create.create1 = -100
                        create.create2 = -100
                        create.create3 = -100
                        create.create4 = -100
                        create.createitem_hp = -100
                        create.createitem_ga = -100
                        for enemyone in EnemyOne_L:
                            EnemyOne_L.remove(enemyone)
                            enemyone_blast1 = Blast1(enemyone.x, enemyone.y)
                            Blast1_L.append(enemyone_blast1)
                        for enemytwo in EnemyTwo_L:
                            EnemyTwo_L.remove(enemytwo)
                            enemytwo_blast1 = Blast1(enemytwo.x, enemytwo.y)
                            Blast1_L.append(enemytwo_blast1)
                        for enemythree in EnemyThree_L:
                            EnemyThree_L.remove(enemythree)
                            enemythree_blast1 = Blast1(enemythree.x, enemythree.y)
                            Blast1_L.append(enemythree_blast1)
                        for enemyfour in EnemyFour_L:
                            EnemyFour_L.remove(enemyfour)
                            enemyfour_blast1 = Blast1(enemyfour.x, enemyfour.y)
                            Blast1_L.append(enemyfour_blast1)

# 충돌체크(플레이어미사일, 적1,2,3,4) #
    for missile2 in Missile2_L:
        for enemyone in EnemyOne_L:
            if collide(missile2, enemyone):
                enemyone.life(100)
                Missile2_L.remove(missile2)
                enemyone_blast3 = Blast3(missile2.x, enemyone.y)
                Blast3_L.append(enemyone_blast3)
                ui.sp(7)
                if (enemyone.HEART == False):
                    EnemyOne_L.remove(enemyone)
                    enemyone_blast1 = Blast1(enemyone.x, enemyone.y)
                    Blast1_L.append(enemyone_blast1)
    for missile2 in Missile2_L:
        for enemytwo in EnemyTwo_L:
            if collide(missile2, enemytwo):
                enemytwo.life(120)
                Missile2_L.remove(missile2)
                enemytwo_blast3 = Blast3(missile2.x, enemytwo.y)
                Blast3_L.append(enemytwo_blast3)
                ui.sp(3)
                if (enemytwo.HEART == False):
                    EnemyTwo_L.remove(enemytwo)
                    enemytwo_blast1 = Blast1(enemytwo.x, enemytwo.y)
                    Blast1_L.append(enemytwo_blast1)
    for missile2 in Missile2_L:
        for enemythree in EnemyThree_L:
            if collide(missile2, enemythree):
                enemythree.life(150)
                Missile2_L.remove(missile2)
                enemythree_blast3 = Blast3(missile2.x, enemythree.y)
                Blast3_L.append(enemythree_blast3)
                ui.sp(5)
                if (enemythree.HEART == False):
                    EnemyThree_L.remove(enemythree)
                    enemythree_blast1 = Blast1(enemythree.x, enemythree.y)
                    Blast1_L.append(enemythree_blast1)
    for missile2 in Missile2_L:
        for enemyfour in EnemyFour_L:
            if collide(missile2, enemyfour):
                enemyfour.life(100)
                Missile2_L.remove(missile2)
                enemyfour_blast3 = Blast3(missile2.x, enemyfour.y)
                Blast3_L.append(enemyfour_blast3)
                ui.sp(3)
                if (enemyfour.HEART == False):
                    EnemyFour_L.remove(enemyfour)
                    enemyfour_blast1 = Blast1(enemyfour.x, enemyfour.y)
                    Blast1_L.append(enemyfour_blast1)

# 충독체크(플레이어 필살기, 중간보스, 최종보스, 적1,2,3,4, 미사일) #
    for enemyone in EnemyOne_L:
        if collide(enemyone, ga1):
            EnemyOne_L.remove(enemyone)
            enemyone_blast1 = Blast1(enemyone.x, enemyone.y)
            Blast1_L.append(enemyone_blast1)
            if ga1.y > 800:
                ga1.y = -200
                ga1.yy = 0
            ui.sp(7)
    for enemyone in EnemyOne_L:
        if collide(enemyone, ga2):
            EnemyOne_L.remove(enemyone)
            enemyone_blast1 = Blast1(enemyone.x, enemyone.y)
            Blast1_L.append(enemyone_blast1)
            if ga2. y > 800:
                ga2.y = -200
                ga2.yy = 0
            ui.sp(7)
    for enemytwo in EnemyTwo_L:
        if collide(enemytwo, ga1):
            EnemyTwo_L.remove(enemytwo)
            enemytwo_blast1 = Blast1(enemytwo.x, enemytwo.y)
            Blast1_L.append(enemytwo_blast1)
            ui.sp(3)
    for enemytwo in EnemyTwo_L:
        if collide(enemytwo, ga2):
            EnemyTwo_L.remove(enemytwo)
            enemytwo_blast1 = Blast1(enemytwo.x, enemytwo.y)
            Blast1_L.append(enemytwo_blast1)
            ui.sp(3)
    for enemythree in EnemyThree_L:
        if collide(enemythree, ga1):
            EnemyThree_L.remove(enemythree)
            enemythree_blast1 = Blast1(enemythree.x, enemythree.y)
            Blast1_L.append(enemythree_blast1)
            ui.sp(5)
    for enemythree in EnemyThree_L:
        if collide(enemythree, ga2):
            EnemyThree_L.remove(enemythree)
            enemythree_blast1 = Blast1(enemythree.x, enemythree.y)
            Blast1_L.append(enemythree_blast1)
            ui.sp(5)
    for enemyfour in EnemyFour_L:
        if collide(enemyfour, ga1):
            EnemyFour_L.remove(enemyfour)
            enemyfour_blast1 = Blast1(enemyfour.x, enemyfour.y)
            Blast1_L.append(enemyfour_blast1)
            ui.sp(3)
    for enemyfour in EnemyFour_L:
        if collide(enemyfour, ga2):
            EnemyFour_L.remove(enemyfour)
            enemyfour_blast1 = Blast1(enemyfour.x, enemyfour.y)
            Blast1_L.append(enemyfour_blast1)
            ui.sp(3)
    for e_missile in E_Missile_L:
        if collide(e_missile, ga1):
            E_Missile_L.remove(e_missile)
    for e_missile in E_Missile_L:
        if collide(e_missile, ga2):
            E_Missile_L.remove(e_missile)

    for middleboss in MiddleBoss_L:
        if collide(middleboss, ga1):
            middleboss.life(5)
            middleboss_blast3 = Blast3(middleboss.x, middleboss.y)
            Blast3_L.append(middleboss_blast3)
            if ga1.y > 800:
                ga1.y = -200
                ga1.yy = 0
            ui.sp(10)
            if (middleboss.HEART == False):
                MiddleBoss_L.remove(middleboss)
                middlebossup_blast3 = Blast3(middleboss.x, middleboss.y + 100)
                middlebossdown_blast3 = Blast3(middleboss.x, middleboss.y - 100)
                Blast3_L.append(middlebossup_blast3)
                Blast3_L.append(middlebossdown_blast3)
    for middleboss in MiddleBoss_L:
        if collide(middleboss, ga2):
            middleboss.life(5)
            middleboss_blast3 = Blast3(middleboss.x, middleboss.y)
            Blast3_L.append(middleboss_blast3)
            if ga2.y > 800:
                ga2.y = -200
                ga2.yy = 0
            ui.sp(10)
            if (middleboss.HEART == False):
                MiddleBoss_L.remove(middleboss)
                middlebossup_blast3 = Blast3(middleboss.x, middleboss.y + 100)
                middlebossdown_blast3 = Blast3(middleboss.x, middleboss.y - 100)
                Blast3_L.append(middlebossup_blast3)
                Blast3_L.append(middlebossdown_blast3)
    for boss in Boss_L:
        if collide(boss, ga1):
            boss.life(5)
            boss_blast3 = Blast3(boss.x, boss.y)
            Blast3_L.append(boss_blast3)
            if ga1.y > 800:
                ga1.y = -200
                ga1.yy = 0
            ui.sp(20)
            if (boss.HEART == False):
                Boss_L.remove(boss)
                create.bossl = False
                bossup_blast3 = Blast3(boss.x, boss.y + 100)
                bossdown_blast3 = Blast3(boss.x, boss.y - 100)
                Blast3_L.append(bossup_blast3)
                Blast3_L.append(bossdown_blast3)
                if (boss.gage < 0):
                    create.create1 = -100
                    create.create2 = -100
                    create.create3 = -100
                    create.create4 = -100
                    create.createitem_hp = -100
                    create.createitem_ga = -100
                    for enemyone in EnemyOne_L:
                        EnemyOne_L.remove(enemyone)
                        enemyone_blast1 = Blast1(enemyone.x, enemyone.y)
                        Blast1_L.append(enemyone_blast1)
                    for enemytwo in EnemyTwo_L:
                        EnemyTwo_L.remove(enemytwo)
                        enemytwo_blast1 = Blast1(enemytwo.x, enemytwo.y)
                        Blast1_L.append(enemytwo_blast1)
                    for enemythree in EnemyThree_L:
                        EnemyThree_L.remove(enemythree)
                        enemythree_blast1 = Blast1(enemythree.x, enemythree.y)
                        Blast1_L.append(enemythree_blast1)
                    for enemyfour in EnemyFour_L:
                        EnemyFour_L.remove(enemyfour)
                        enemyfour_blast1 = Blast1(enemyfour.x, enemyfour.y)
                        Blast1_L.append(enemyfour_blast1)
    for boss in Boss_L:
        if collide(boss, ga2):
            boss.life(5)
            boss_blast3 = Blast3(boss.x, boss.y)
            Blast3_L.append(boss_blast3)
            if ga2.y > 800:
                ga2.y = -200
                ga2.yy = 0
            ui.sp(20)
            if (boss.HEART == False):
                Boss_L.remove(boss)
                create.bossl = False
                bossup_blast3 = Blast3(boss.x, boss.y + 100)
                bossdown_blast3 = Blast3(boss.x, boss.y - 100)
                Blast3_L.append(bossup_blast3)
                Blast3_L.append(bossdown_blast3)
                if (boss.gage < 0):
                    create.create1 = -100
                    create.create2 = -100
                    create.create3 = -100
                    create.create4 = -100
                    create.createitem_hp = -100
                    create.createitem_ga = -100
                    for enemyone in EnemyOne_L:
                        EnemyOne_L.remove(enemyone)
                        enemyone_blast1 = Blast1(enemyone.x, enemyone.y)
                        Blast1_L.append(enemyone_blast1)
                    for enemytwo in EnemyTwo_L:
                        EnemyTwo_L.remove(enemytwo)
                        enemytwo_blast1 = Blast1(enemytwo.x, enemytwo.y)
                        Blast1_L.append(enemytwo_blast1)
                    for enemythree in EnemyThree_L:
                        EnemyThree_L.remove(enemythree)
                        enemythree_blast1 = Blast1(enemythree.x, enemythree.y)
                        Blast1_L.append(enemythree_blast1)
                    for enemyfour in EnemyFour_L:
                        EnemyFour_L.remove(enemyfour)
                        enemyfour_blast1 = Blast1(enemyfour.x, enemyfour.y)
                        Blast1_L.append(enemyfour_blast1)


# 충돌체크(적 미사일, 플레이어) #
    for e_missile in E_Missile_L:
        if collide(e_missile, player):
            if (player.HEART == 1):
                E_Missile_L.remove(e_missile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60
                ui.draw()

# 충돌체크(중간보스 미사일, 플레이어) #
    for md_missile in MD_Missile_L:
        if collide(md_missile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_missile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60
                ui.draw()
    for md_Rmissile in MD_Missile_L:
        if collide(md_Rmissile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_Rmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for md_RRmissile in MD_Missile_L:
        if collide(md_RRmissile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_RRmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for md_Lmissile in MD_Missile_L:
        if collide(md_Lmissile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_Lmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for md_LLmissile in MD_Missile_L:
        if collide(md_LLmissile, player):
            if (player.HEART == 1):
                MD_Missile_L.remove(md_LLmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60


# 충돌체크(최종보스 미사일, 플레이어) #
    for b_missile in B_Missile_L:
        if collide(b_missile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_missile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for b_Dmissile in B_Missile_L:
        if collide(b_Dmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_Dmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for b_DOmissile in B_Missile_L:
        if collide(b_DOmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_DOmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for b_DOWmissile in B_Missile_L:
        if collide(b_DOWmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_DOWmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60
                ui.Die()

    for b_DOWNmissile in B_Missile_L:
        if collide(b_DOWNmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_DOWNmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for b_Cmissile in B_Missile_L:
        if collide(b_Cmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_Cmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for b_Rmissile in B_Missile_L:
        if collide(b_Rmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_Rmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for b_RRmissile in B_Missile_L:
        if collide(b_RRmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_RRmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for b_Lmissile in B_Missile_L:
        if collide(b_Lmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_Lmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

    for b_LLmissile in B_Missile_L:
        if collide(b_LLmissile, player):
            if (player.HEART == 1):
                B_Missile_L.remove(b_LLmissile)
                Player.attacks(player)
                player.life(1)
            if (player.HEART == 0):
                player.x = 400
                player.y = -60

def draw(frame_time):
    clear_canvas()
    map.draw()
    hp.draw()
    hpbar.draw()
    ga_ui.draw()

    for enemyone in EnemyOne_L:
        enemyone.draw()
     #   enemyone.draw_bb()
    for enemytwo in EnemyTwo_L:
        enemytwo.draw()
     #   enemytwo.draw_bb()
    for enemythree in EnemyThree_L:
        enemythree.draw()
     #   enemythree.draw_bb()
    for enemyfour in EnemyFour_L:
        enemyfour.draw()
     #   enemyfour.draw_bb()
    for middleboss in MiddleBoss_L:
        middleboss.draw()
     #   middleboss.draw_bb()
    for boss in Boss_L:
        boss.draw()
      #  boss.draw_bb()
    for item_hp in Item_HP_L:
        item_hp.draw()
       # item_hp.draw_bb()
    for item_ga in Item_GA_L:
        item_ga.draw()
        #item_ga.draw_bb()

    player.draw()
    #player.draw_bb()

    for missile1 in Missile1_L:
        missile1.draw()
     #   missile1.draw_bb()
    for missile2 in Missile2_L:
        missile2.draw()
     #   missile2.draw_bb()

    for e_missile in E_Missile_L:
        e_missile.draw()
     #   e_missile.draw_bb()
    for md_missile in MD_Missile_L:
        md_missile.draw()
      #  md_missile.draw_bb()
    for md_Rmissile in MD_Missile_L:
        md_Rmissile.draw()
     #   md_Rmissile.draw_bb()
    for md_RRmissile in MD_Missile_L:
        md_RRmissile.draw()
     #   md_RRmissile.draw_bb()
    for md_Lmissile in MD_Missile_L:
        md_Lmissile.draw()
    #    md_Lmissile.draw_bb()
    for md_LLmissile in MD_Missile_L:
        md_LLmissile.draw()
     #   md_LLmissile.draw_bb()
    for b_missile in B_Missile_L:
        b_missile.draw()
     #   b_missile.draw_bb()
    for b_Dmissile in B_Missile_L:
        b_Dmissile.draw()
     #   b_Dmissile.draw_bb()
    for b_DOmissile in B_Missile_L:
        b_DOmissile.draw()
     #   b_DOmissile.draw_bb()
    for b_DOWmissile in B_Missile_L:
        b_DOWmissile.draw()
      #  b_DOWmissile.draw_bb()
    for b_DOWNmissile in B_Missile_L:
        b_DOWNmissile.draw()
      #  b_DOWNmissile.draw_bb()
    for b_Cmissile in B_Missile_L:
        b_Cmissile.draw()
     #   b_Cmissile.draw_bb()
    for b_Rmissile in B_Missile_L:
        b_Rmissile.draw()
      #  b_Rmissile.draw_bb()
    for b_RRmissile in B_Missile_L:
        b_RRmissile.draw()
     #   b_RRmissile.draw_bb()
    for b_Lmissile in B_Missile_L:
        b_Lmissile.draw()
      #  b_Lmissile.draw_bb()
    for b_LLmissile in B_Missile_L:
        b_LLmissile.draw()
    #    b_LLmissile.draw_bb()


    for blast1 in Blast1_L:
        blast1.draw()
    for blast2 in Blast2_L:
        blast2.draw()
    for blast3 in Blast3_L:
        blast3.draw()

    ga1.draw()
   # ga1.draw_bb()
    ga2.draw()
   # ga2.draw_bb()

    ui.draw()

    update_canvas()


# 종료시 화면 설정
# 아이템 설정(hp, 필살기, 미사일)
