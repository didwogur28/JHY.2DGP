from pico2d import *

class Blast1:
    TIME_PER_ACTION = 0.7
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 12

    blastsound1 = None
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.total_frame = 0.0
        self.life_time = 0.0
        if Blast1.image == None:
            Blast1.image = load_image('object/Missile/Blast.png')
        if self.blastsound1 == None:
            self.blastsound1 = load_wav('object\\Sound\\Enemybombsound.wav')
            self.blastsound1.set_volume(6)

    def update(self, frame_time):
        self.life_time += frame_time
        self.total_frame += Blast1.FRAMES_PER_ACTION * Blast1.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frame) % 12
        self.blasts1()
        if (self.frame == 11):
            return True
        else:
            return False

    def blasts1(self):
        self.blastsound1.play()

    def draw(self):
        self.image.clip_draw(self.frame * 100,0, 100, 150, self.x, self.y)

class Blast2:
    TIME_PER_ACTION = 0.7
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 12

    blastsound2 = None
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.total_frame = 0.0
        self.life_time = 0.0
        if Blast2.image == None:
            Blast2.image = load_image('object/Missile/Blast.png')
        if self.blastsound2 == None:
            self.blastsound2 = load_wav('object\\Sound\\Bossbombsound.wav')
            self.blastsound2.set_volume(6)

    def update(self, frame_time):
        self.life_time += frame_time
        self.total_frame += Blast2.FRAMES_PER_ACTION * Blast2.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frame) % 12
        self.blasts2()
        if (self.frame == 11):
            return True
        else:
            return False

    def blasts2(self):
        self.blastsound2.play()

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 150, self.x, self.y)

class Blast3:
    TIME_PER_ACTION = 0.7
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    blast2sound = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.total_frame = 0.0
        self.life_time = 0.0
        self.image = load_image('object/Missile/Blast3.png')

    def update(self, frame_time):
        self.life_time += frame_time
        self.total_frame += Blast2.FRAMES_PER_ACTION * Blast2.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frame) % 6
        if (self.frame == 5):
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 70,0, 70, 100, self.x, self.y)


