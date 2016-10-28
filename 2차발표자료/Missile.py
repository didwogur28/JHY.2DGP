from pico2d import *
__author__ = 'user'

class Missile1:
    def __init__(self,x, y):
        self.x = x
        self.y = y

    def update(self):
        self.image = load_image('object/Missile/Missile1.png')
        self.y += 50

    def draw(self):
        self.image.draw(self.x, self.y)

class Missile2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.image = load_image('object/Missile/Missile2.png')
        self.y += 50

    def draw(self):
        self.image.draw(self.x, self.y)

class Missile3:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.image = load_image('object/Missile/Missile3.png')
        self.y += 50

    def draw(self):
        self.image.draw(self.x, self.y)

class GrandAttack1:
    global grandattck1
    grandattack1 = False

    def __init__(self):
        self.x = 200
        self.y = -200

    def update(self):
        global grandattck1
        self.image = load_image('object/Player/GrateAttack1.png')
        if (grandattck1 == True):
            self.y += 20
        if self.y > 1000:
            self.y = -200
            grandattck1 = False

    def handle_event(self, event):
        global grandattck1
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            grandattck1 = True

    def draw(self):
        self.image.draw(self.x, self.y)

class GrandAttack2:
    global ga2
    ga2 = False

    def __init__(self):
        self.x = 600
        self.y = -200

    def update(self):
        global ga2
        self.image = load_image('object/Player/GrateAttack2.png')
        if (ga2 == True):
            self.y += 20
        if self.y > 1000:
            self.y = -200
            ga2 = False

    def handle_event(self, event):
        global ga2
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            ga2 = True

    def draw(self):
        self.image.draw(self.x, self.y)