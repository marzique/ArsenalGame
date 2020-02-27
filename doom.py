"""
https://gist.github.com/limdingwen/c8bb49474de7765f92ee198a1f0f31d5
"""


# X is left-right
# Y is forwards-backwards
# Z is up-down

import pygame
import math
from src.player import Player
from src.engine import Control


player = Player('tarn')
controller = Control(player)


if __name__ == '__main__':
    controller.run()
