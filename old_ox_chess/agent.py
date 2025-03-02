from collections import defaultdict
import random

class Agent:

    def __init__(self):
        self.e_greedy_v = 0.1
        self.q = defaultdict(int)
        self.v = defaultdict(int)
        self.vct = defaultdict(int)
        self.pi = defaultdict(lambda: [1/9 for _ in range(9)])
        self.action_space = [(x, y) for x in range(3) for y in range(3)]
        self.memory = []

    def e_greedy(self,state):
        action_reward = [self.q[(state, ac)] for ac in self.action_space]
        best_action = action_reward.index(max(action_reward))

        self.pi[state] = [0.03333 for _ in range(9)]
        self.pi[state][best_action] += 0.7


    def run(self, state):

        action_prob = self.pi[state]
        action = random.choices(self.action_space, weights=action_prob)[0]
        return action
    
    def feedback(self, state, action, r):
        self.memory.append([state, action, r])
    
    def eval(self):
        Q = 0
        G = 0
        gamma = 0.9
        for m in self.memory:
            s, a, r = m
            n = max(self.vct[s], 1)  # 当前状态的访问次数

            # update Value
            G = gamma * G + r
            self.v[s] = \
            (self.v[s] * (n / (n + 1)))\
            + (G / n + 1) 

            # update Q
            Q = gamma * Q + r
            self.q[(s,a)] = \
            (self.q[(s,a)] * (n / (n+1)))\
            + (Q / n+1)  

            self.e_greedy(s)

            self.vct[s] += 1  # 增加访问次数
        
        self.memory = []
    
