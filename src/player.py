"""Player data"""
from .helpers import rad
import math


class Player:
    SPEED = 0.05
    ROT_SPEED = 2
    TOP_ZOOM = 5
    RAY_LENGTH = 0.1 / TOP_ZOOM
    COLOR = (0, 255, 0)
    RAY_COLOR = (255, 0, 0)
    MOUSE_SENSITIVITY = 0.15


    def __init__(self, nickname):
        self.health = 100
        self.armor = 100
        self.pos = (0.0, 0.0) 
        self.rot = 0.0 # 0 is north, clockwise, degrees
        self.nickname = nickname
        print(f'{self.nickname} welcome!')


    def move(self, mult, rot_disp):
        x = self.pos[0] + math.sin(rad(self.rot + rot_disp)) * self.SPEED * mult
        y = self.pos[1] + math.cos(rad(self.rot + rot_disp)) * self.SPEED * mult
        self.pos = (x, y)
