"""Player data"""


class Player:
    def __init__(self, nickname):
        self.health = 100
        self.armor = 100
        self.pos = (0.0, 0.0) 
        self.rot = 0.0 # 0 is north, clockwise, degrees
        self.nickname = nickname
        print(f'{self.nickname} welcome!')

