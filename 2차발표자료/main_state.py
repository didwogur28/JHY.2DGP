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

    def update(self):
        self.down = (self.down + 0.02 * self.speed) % self.image.h
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
    global map, player, enemyone, enemytwo, enemythree, middleboss, boss, ga1, ga2
    map = Map(800, 750)
    player = Player()
    enemyone = EnemyOne()
    enemytwo = EnemyTwo()
    enemythree = EnemyThree()
    middleboss = MiddleBoss()
    boss = Boss()
    ga1 = GrandAttack1()
    ga2 = GrandAttack2()

def exit():
    global map, player, enemyone, enemytwo, enemythree, middleboss, boss, ga1, ga2
    del(enemyone)
    del(enemytwo)
    del(enemythree)
    del(player)
    del(map)
    del(middleboss)
    del(boss)
    del(ga1)
    del(ga2)

def update():
    map.update()
    player.update()
    enemyone.update()
    enemytwo.update()
    enemythree.update()
    middleboss.update()
    boss.update()
    ga1.update()
    ga2.update()

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

    delay(0.04)
    update_canvas()

def main():
    enter()

    running = True;
    while running:
        handle_events()
        update()
        draw()

    exit()

if __name__ == '__main__':
    main()

