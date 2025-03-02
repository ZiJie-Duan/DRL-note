from game import OXGame
from game2 import OXGame2

ox = OXGame2()
ox.pprint(*ox.o_move(1))
ox.pprint(*ox.x_move(5))
ox.pprint(*ox.o_move(4))
ox.pprint(*ox.x_move(7))
ox.pprint(*ox.o_move(2))
ox.pprint(*ox.x_move(9))
print(ox.x_move(3))