from src.player import Player
from src.engine import Control


player = Player('tarn')
controller = Control(player)


if __name__ == '__main__':
    controller.run()
