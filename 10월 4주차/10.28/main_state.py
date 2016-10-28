import game_framework
import title_state
from pico2d import *
from Player import Player
from Enemy import EnemyOne
from Enemy import EnemyTwo
from Enemy import EnemyThree
from Enemy import Boss
from Enemy import MiddleBoss
from Missile import GrandAttack1
from Missile import GrandAttack2

name = "MainState"

running = None
player = None



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

def enter():
    global timer, map, player, enemyone, enemytwo, enemythree, middleboss, boss, ga1, ga2, EnemyOne_L,\
        EnemyTwo_L, EnemyThree_L, MiddleBoss_L, Boss_L, Missile1_L, Missile2_L, Missile3_L, GrandAttack_L

    map = Map(800, 750)

    timer = Timer()
    player = Player()
    enemyone = EnemyOne()
    enemytwo = EnemyTwo()
    enemythree = EnemyThree()
    middleboss = MiddleBoss()
    boss = Boss()
    ga1 = GrandAttack1()
    ga2 = GrandAttack2()

def exit():
    global timer, map, player, enemyone, enemytwo, enemythree, middleboss, boss, ga1, ga2, EnemyOne_L,\
        EnemyTwo_L, EnemyThree_L, MiddleBoss_L, Boss_L, Missile1_L, Missile2_L, Missile3_L, GrandAttack_L
    del(timer)
    del(enemyone)
    del(enemytwo)
    del(enemythree)
    del(player)
    del(map)
    del(middleboss)
    del(boss)
    del(ga1)
    del(ga2)
    del(EnemyOne_L)
    del(EnemyTwo_L)
    del(EnemyThree_L)
    del(MiddleBoss_L)
    del(Boss_L)
    del(GrandAttack_L)
    close_canvas()

def update(frame_time):
    timer.update(frame_time)

    map.update(frame_time)
    player.update(frame_time)
    enemyone.update(frame_time)
    enemytwo.update(frame_time)
    enemythree.update(frame_time)
    middleboss.update(frame_time)
    boss.update(frame_time)
    ga1.update(frame_time)
    ga2.update(frame_time)

def draw():
    clear_canvas()
    map.draw()
    player.draw()
    enemyone.draw()
    enemytwo.draw()
    enemythree.draw()
    middleboss.draw()
    boss.draw()
    ga1.draw()
    ga2.draw()

    delay(0.02)
    update_canvas()

def main(frame_time):
    enter()

    running = True;
    while running:
        handle_events()
        update(frame_time)
        draw()

    exit()