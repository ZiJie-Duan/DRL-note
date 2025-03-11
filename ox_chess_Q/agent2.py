from collections import defaultdict
import random
import json

class Agent2Q:

    def __init__(self):
        self.e_greedy_v = 0.1
        self.q = defaultdict(int)
        self.action_space = [x for x in range(1,10)]

    def valid_action_sapce(self, state):
        valid_action_num = 0
        valid_action_space_index = []
        for i, v in enumerate(state):
            if v == "0":
                valid_action_space_index.append(i)
                valid_action_num += 1
        return [self.action_space[i] for i in valid_action_space_index]
    
    
    def get_max_from_q(self, state):

        valid_actions = self.valid_action_sapce(state)
        if valid_actions == []:
            return None, None

        max_a = random.choice(valid_actions)
        max_a_q = self.q[(state, max_a)]

        for a in valid_actions:
            t_q = self.q[(state,a)]
            if t_q > max_a_q:
                max_a = a
                max_a_q = t_q
        
        return max_a, max_a_q


    def run(self, state):

        if random.random() < self.e_greedy_v:
            return random.choice(self.action_space)
        
        max_a, _ = self.get_max_from_q(state)
        return max_a
    

    def rotate(self, state):
        ns = []
        ns.append(state[2])
        ns.append(state[5])
        ns.append(state[8])
        ns.append(state[1])
        ns.append(state[4])
        ns.append(state[7])
        ns.append(state[0])
        ns.append(state[3])
        ns.append(state[6])
        return "".join(ns)
    
    def rotate_point(self, action):
        map = [7,4,1,8,5,2,9,6,3]
        return map[action - 1]
 
    def eval(self, state, action, r, next_state):

        s = state
        a = action
        r = r
        ns = next_state

        for _ in range(4):
            s = self.rotate(s)
            a = self.rotate_point(a)
            ns = self.rotate(ns)

            _, next_max_q = self.get_max_from_q(ns)

            if next_max_q == None:
                return

            self.q[(s, a)] += 0.8 * ((float(r) + 0.9 * next_max_q)-self.q[(s, a)])

