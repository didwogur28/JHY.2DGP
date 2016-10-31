from pico2d import *
import random

__author__ = 'user'

EnemyOne_L = []
EnemyTwo_L = []
EnemyThree_L = []
MiddleBoss_L = []
Boss_L= []

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

class EnemyTwo:
    PIXEL_PER_METER = (10.0 / 0.2)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    LEFTDOWN_RUN, RIGHTUP_RUN, LEFTDOWN_STAND, RIGHTUP_STAND = 0, 1, 2, 3

    image = None

    def __init__(self):
        if EnemyTwo.image == None:
            EnemyTwo.image = load_image('object/Enemy/Enemy2.png')
        self.x, self.y = random.randint(800, 1000), random.randint(1000, 1100)
        self.xdir = 0
        self.ydir = 0
        self.frame = random.randint(0, 6)
        self.run_frame = 0
        self.stand_frame = 0
        self.total_frames = 0.0
        self.state = self.LEFTDOWN_RUN
        self.name = 'enemytwo'

    def handle_leftdown_run(self):
        self.xdir = -1
        self.ydir = -1
        self.run_frame += 1
        if self.y < 100:
            self.state = self.RIGHTUP_RUN
        if self.x < 100:
            self.state = self.RIGHTUP_RUN
        if self.run_frame == 200:
            self.state = self.LEFTDOWN_STAND
            self.stand_frame = 0
    def handle_leftdown_stand(self):
        self.stand_frame += 1
        if self.stand_frame == 50:
            self.state = self.LEFTDOWN_RUN
            self.run_frame = 0

    def handle_rightup_run(self):
        self.xdir = 1
        self.ydir = 1
        self.run_frame += 1
        if self.y > 700:
            self.state = self.LEFTDOWN_RUN
        if self.x > 700:
            self.state = self.LEFTDOWN_RUN
        if self.run_frame == 200:
            self.state = self.RIGHTUP_STAND
            self.stand_frame = 0
    def handle_rightup_stand(self):
        self.stand_frame += 1
        if self.stand_frame == 50:
            self.state = self.RIGHTUP_RUN
            self.run_frame = 0

    handle_state = {
        LEFTDOWN_RUN: handle_leftdown_run, RIGHTUP_RUN: handle_rightup_run,
        LEFTDOWN_STAND: handle_leftdown_stand, RIGHTUP_STAND:handle_rightup_stand
        }

    def update(self,frame_time):
        distance = EnemyTwo.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyTwo.FRAMES_PER_ACTION * EnemyTwo.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)

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

    DOWN_RUN, UP_RUN, DOWN_STAND, UP_STAND = 0, 1, 2, 3

    image = None

    def __init__(self):
        if EnemyThree.image == None:
            EnemyThree.image = load_image('object/Enemy/Enemy3.png')
        self.x, self.y = random.randint(70, 730), random.randint(1000, 1100)
        self.xdir = 0
        self.ydir = 0
        self.frame = random.randint(0, 4)
        self.run_frame = 0
        self.stand_frame = 0
        self.total_frames = 0.0
        self.state = self.DOWN_RUN
        self.name = 'enemythree'

    def handle_down_run(self):
        self.ydir = -1
        self.run_frame += 1
        if self.y < 400:
            self.state = self.UP_RUN
            self.y = 400
        if self.run_frame == 80:
            self.state = self.DOWN_STAND
            self.stand_frame = 0
    def handle_down_stand(self):
        self.stand_frame += 1
        if self.stand_frame == 80:
            self.state = self.DOWN_RUN
            self.run_frame = 0

    def handle_up_run(self):
        self.ydir = 1
        self.run_frame += 1
        if self.y  > 700:
            self.state = self.DOWN_RUN
            self.y = 700
        if self.run_frame == 80:
            self.state = self.UP_STAND
            self.stand_frame = 0
    def handle_up_stand(self):
        self.stand_frame += 1
        if self.stand_frame == 80:
            self.state = self.UP_RUN
            self.run_frame = 0

    handle_state = {
        DOWN_RUN: handle_down_run, UP_RUN: handle_up_run, DOWN_STAND: handle_down_stand, UP_STAND: handle_up_stand}

    def update(self,frame_time):
        distance = EnemyThree.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyThree.FRAMES_PER_ACTION * EnemyThree.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)

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

    RIGHTDOWN_RUN, LEFTUP_RUN, RIGHTDOWN_STAND, LEFTUP_STAND = 0, 1, 2, 3

    image = None

    def __init__(self):
        if EnemyFour.image == None:
            EnemyFour.image = load_image('object/Enemy/Enemy2.png')
        self.x, self.y = random.randint(-200, -100), random.randint(1000, 1100)
        self.xdir = 0
        self.ydir = 0
        self.frame = random.randint(0, 6)
        self.run_frame = 0
        self.stand_frame = 0
        self.total_frames = 0.0
        self.state = self.RIGHTDOWN_RUN
        self.name = 'enemyfour'


    def handle_rightdown_run(self):
        self.xdir = 1
        self.ydir = -1
        self.run_frame += 1
        if self.y < 100:
            self.state = self.LEFTUP_RUN
        if self.x > 700:
            self.state = self.LEFTUP_RUN
        if self.run_frame == 200:
            self.state = self.RIGHTDOWN_STAND
            self.stand_frame = 0
    def handle_rightdown_stand(self):
        self.stand_frame += 1
        if self.stand_frame == 50:
            self.state = self.RIGHTDOWN_RUN
            self.run_frame = 0

    def handle_leftup_run(self):
        self.xdir = -1
        self.ydir = 1
        self.run_frame += 1
        if self.y > 700:
            self.state = self.RIGHTDOWN_RUN
        if self.x < 100:
            self.state = self.RIGHTDOWN_RUN
        if self.run_frame == 200:
            self.state = self.LEFTUP_STAND
            self.stand_frame = 0
    def handle_leftup_stand(self):
        self.stand_frame += 1
        if self.stand_frame == 50:
            self.state = self.LEFTUP_RUN
            self.run_frame = 0

    handle_state = {
        RIGHTDOWN_RUN: handle_rightdown_run, LEFTUP_RUN: handle_leftup_run,
        RIGHTDOWN_STAND: handle_rightdown_stand, LEFTUP_STAND: handle_leftup_stand
        }

    def update(self,frame_time):
        distance = EnemyFour.RUN_SPEED_PPS * frame_time
        self.total_frames += EnemyFour.FRAMES_PER_ACTION * EnemyFour.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)

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
