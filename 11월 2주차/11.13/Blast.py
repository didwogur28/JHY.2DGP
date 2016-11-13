from pico2d import *

class Blast:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 12

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.total_frame = 0.0
        self.life_time = 0.0
        self.image = load_image('object/Missile/Blast.png')

    def update(self, frame_time):
        self.life_time += frame_time
        self.total_frame += Blast.FRAMES_PER_ACTION * Blast.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frame) % 12
        if (self.frame == 11):
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 100,0, 100, 150, self.x, self.y)
