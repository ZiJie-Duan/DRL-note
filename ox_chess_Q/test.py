from game2 import OXGame2

import time

ox = OXGame2()

start_time = time.time()
ox.o_move(1)
print(f"ox.o_move(1) took {time.time() - start_time} seconds")

start_time = time.time()
ox.x_move(5)
print(f"ox.x_move(5) took {time.time() - start_time} seconds")

start_time = time.time()
ox.o_move(4)
print(f"ox.o_move(4) took {time.time() - start_time} seconds")

start_time = time.time()
ox.x_move(7)
print(f"ox.x_move(7) took {time.time() - start_time} seconds")

start_time = time.time()
ox.o_move(2)
print(f"ox.o_move(2) took {time.time() - start_time} seconds")

start_time = time.time()
ox.x_move(9)
print(f"ox.x_move(9) took {time.time() - start_time} seconds")

start_time = time.time()
print(ox.x_move(3))
print(f"ox.x_move(3) took {time.time() - start_time} seconds")