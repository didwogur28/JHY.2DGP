from pico2d import *
import random
from Enemy import EnemyOne
from Enemy import EnemyTwo
from Enemy import EnemyThree
from Enemy import EnemyFour
from Enemy import MiddleBoss
from Enemy import Boss


EnemyOne_L = []
EnemyTwo_L = []
EnemyThree_L = []
EnemyFour_L = []
MiddleBoss_L = []
Boss_L= []


class Timer:
    def __init__(self):
        self.time1 = 0.0
        self.time2 = 0.0
        self.time3 = 0.0
        self.time4 = 0.0
        self.timemiddle = 0.0
        self.timeboss = 0.0
        self.middlel = False
        self.bossl = False

    def update(self, frame_time):
        self.time1 += frame_time
        self.time2 += frame_time
        self.time3 += frame_time
        self.time4 += frame_time
        self.timemiddle += frame_time
        self.timeboss += frame_time
        self.CEnemyOne()
        self.CEnemyTwo()
        self.CEnemyThree()
        self.CEnemyFour()
        self.CMiddleBoss()
        self.CBoss()

    def CEnemyOne(self):
        if (self.time1 >= 3 and self.bossl == False):
            nEnemyOne = EnemyOne()
            EnemyOne_L.append(nEnemyOne)
            self.time1 = 0.0

    def CEnemyTwo(self):
        if (self.time2 >= 6 and self.bossl == False):
            nEnemyTwo = EnemyTwo()
            EnemyTwo_L.append(nEnemyTwo)
            self.time2 = 0.0

    def CEnemyThree(self):
        if (self.time3 >= 5 and self.bossl == False):
            nEnemyThree = EnemyThree()
            EnemyThree_L.append(nEnemyThree)
            self.time3 = 0.0

    def CEnemyFour(self):
        if (self.time4 >= 6 and self.bossl == False):
            nEnemyFour = EnemyFour()
            EnemyFour_L.append(nEnemyFour)
            self.time4 = 0.0

    def CMiddleBoss(self):
        if (self.timemiddle >= 40 and self.bossl == False):
            self.middlel = True
            nMiddleBoss = MiddleBoss()
            MiddleBoss_L.append(nMiddleBoss)
            self.timemiddle = 0.0

    def CBoss(self):
        if (self.timeboss >= 80 and self.bossl == False):
            if self.middlel == True:
                self.middlel = False
            self.bossl = True
            nBoss = Boss()
            Boss_L.append(nBoss)
            self.timeboss = 0.0