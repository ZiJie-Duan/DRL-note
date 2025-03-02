from game import OXGame
from agent import Agent


class RFL:

    def __init__(self, round = 1000) -> None:
        self.round = round
        self.game = OXGame()
        self.a1 = Agent()
        self.a2 = Agent()
    
    def o_state(self, info):
        state = ""
        for row in info[1]:
            for cell in row:
                if cell == 1:
                    state += "2"
                elif cell == 2:
                    state += "1"
                else:
                    state += "0"
        return state
    
    def x_state(self, info):
        state = ""
        for row in info[1]:
            for cell in row:
                state += str(cell)
        return state
    
    def run_step(self):

        self.game.init_game()
        # init state
        info = None
        state = self.x_state(self.game.get_state(True)) 

        while True:

            while True:
                action = self.a1.run(state)
                f = self.game.x_move(*action)
                #self.game.pprint(*f)
                if f[0]:
                    info = f
                    state = self.x_state(f)
                    self.a1.feedback(self.x_state(f),f[3],f[4])
                    break
                self.a1.feedback(self.x_state(f),f[3],f[4])

            if info[-1]:
                break

            while True:
                action = self.a2.run(state)
                f = self.game.o_move(*action)
                #self.game.pprint(*f)
                if f[0]:
                    info = f
                    state = self.o_state(f)
                    self.a2.feedback(self.o_state(f),f[3],f[4])
                    break
                self.a2.feedback(self.o_state(f),f[3],f[4])
            
            if info[-1]:
                break

        self.a1.eval()
        self.a2.eval()

    def run_sim(self):
        for i in range(self.round):
            print(i)
            self.run_step()
        
        for k, v in self.a1.q.items():
            print(f"{k} : {v}")

rfl = RFL(20000)
rfl.run_sim()
# rfl.game.init_game()
# rfl.game.x_move(0,0)
# rfl.game.o_move(1,1)
# info = rfl.game.x_move(2,1)
# rfl.game.pprint(*info)
# print(rfl.x_state(info))
# print(rfl.o_state(info))
        
