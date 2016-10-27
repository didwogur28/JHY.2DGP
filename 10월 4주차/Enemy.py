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