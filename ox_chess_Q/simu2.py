from game2 import OXGame2
from agent2 import Agent2Q
S = 0
A = 1
R = 2
SD = 3
END = 4

class RFL2:

    def __init__(self, round = 1000) -> None:
        self.round = round
        self.game = OXGame2()
        self.a1 = Agent2Q()
        self.a2 = Agent2Q()

    def inv_state(self, state):
        res = ""
        for s in state:
            if s == "1":
                res += "2"
            elif s == "2":
                res += "1"
            else:
                res += "0"
        return res


    def run_step(self, v = False):
        self.game.init_game()
        s,a,r,sd,end = (None,None,None,None,None)

        s = self.game.get_board_state()

        while True:

            while True:
                a = self.a1.run(s)
                s, a, r, sd ,end = self.game.x_move(a)
                #self.game.pprint(s,a,r,sd,end)
                if s != sd:
                    if v:
                        self.game.pprint(s,a,r,sd,end)
                        print("a1:", s)
                    self.a1.eval(s,a,r, sd)
                    s = sd
                    break
                self.a1.eval(s,a,r, sd)

            if end:
                break

            while True:
                a = self.a1.run(self.inv_state(s))
                s, a, r, sd ,end = self.game.o_move(a)
                #self.game.pprint(s,a,r,sd,end)
                if s != sd:
                    if v:
                        self.game.pprint(s,a,r,sd,end)
                        print("a2:",self.inv_state(s))
                    self.a1.eval(self.inv_state(s),a,r, sd)
                    s = sd
                    break
                self.a1.eval(self.inv_state(s),a,r, sd)

            if end:
                break


    def run_sim(self):
        for i in range(self.round):
            if i % 2000 == 0:
                print(i)
            if i > self.round - 100:
                self.run_step(v = True)
            else:
                self.run_step()

        # q,c = self.a2.get_qv()
        #self.a1.mix_q(q,c)
        
        # for k, v in self.a1.q.items():
        #     print(f"{k} : {v}")


    def eval_step(self, a1, a2):
        self.game.init_game()
        s,a,r,sd,end = (None,None,None,None,None)

        s = self.game.get_board_state()

        while True:

            while True:
                a = a1.run(s)
                s, a, r, sd ,end = self.game.x_move(a)
                if s != sd:
                    #self.game.pprint(s,a,r,sd,end)
                    s = sd
                    break

            if end and r >= 1:
                #print("A1 Win!") 
                return a1
            elif end:
                return None

            while True:
                a = a2.run(self.inv_state(s))
                s, a, r, sd ,end = self.game.o_move(a)
                if s != sd:
                    #self.game.pprint(s,a,r,sd,end)
                    s = sd
                    break

            if end and r >= 1:
                #print("A2 Win!")
                return a2
            elif end:
                return None

    def run_eval(self, round = 100):
        a1 = self.a1
        random_agent= self.a2

        a1c = 0
        bc = 0
        a2c = 0

        for _ in range(round):
            r = self.eval_step(a1,random_agent)
            if r == a1:
                a1c += 1
            elif r == random_agent:
                a2c += 1
            else:
                bc += 1
        
        print(f"{a1c}:{bc}:{a2c}")
        return (a1c, bc, a2c)


# Initialize an empty list to store evaluation results
el = []
# Loop 3 times to create and evaluate RFL2 instances
for _ in range(1):
    # Create a new instance of RFL2 with a parameter of 500000
    rfl = RFL2(500000)
    # Run the simulation for the current instance
    rfl.run_sim()
    # Append the evaluation results of the current instance to the results list
    el.append(rfl.run_eval(1000))

print(f"Report: {sum([e[0] for e in el])/30:.2f}% : {sum([e[1] for e in el])/30:.2f}% : {sum([e[2] for e in el])/30:.2f}%")

while True:
    rfl.game.init_game()
    while True:
        user_input = input("请输入您的动作（1-9），或输入'q'结束：")
        if user_input.lower() == 'q':
            print("游戏结束！")
            break

        try:
            action = int(user_input)
            if action not in range(1, 10):
                raise ValueError("动作必须在1到9之间。")
        except ValueError as e:
            print(e)
            continue

        s,a,r,sd,end = rfl.game.x_move(action)
        if end:
            print("游戏结束！")
            break
        
        while True:
            a1_action = rfl.a1.run(rfl.inv_state(s))
            s,a,r,sd,end = rfl.game.o_move(a1_action)
            if s != sd:
                break
        if end:
            print("游戏结束！")
            break

        rfl.game.pprint(s, a, r, sd, end)
    
    rfl.game.pprint(s, a, r, sd, end)


# rfl.game.init_game()
# rfl.game.x_move(0,0)
# rfl.game.o_move(1,1)
# info = rfl.game.x_move(2,1)
# rfl.game.pprint(*info)
# print(rfl.x_state(info))
# print(rfl.o_state(info))
        


