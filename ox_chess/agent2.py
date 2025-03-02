from collections import defaultdict
import random
import json

class Agent2:

    def __init__(self):
        self.e_greedy_v = 0.1
        self.q = defaultdict(int)
        self.v = defaultdict(int)
        self.vct = defaultdict(int)
        self.qct = defaultdict(int)
        self.pi = defaultdict(lambda: [1/9 for _ in range(9)])
        self.action_space = [x for x in range(1,10)]
        self.memory1 = []
        self.memory2 = []

    def e_greedy(self,state):
        action_reward = [self.q[(state, ac)] for ac in self.action_space]
        best_action = action_reward.index(max(action_reward))

        self.pi[state] = [0.088888 for _ in range(9)]
        self.pi[state][best_action] += 0.2


    def run(self, state, mod="t"):
        action_prob = self.pi[state]
        if mod == "t":
            action = random.choices(self.action_space, weights=action_prob)[0]
            return action
        else:
            action = self.action_space[action_prob.index(max(action_prob))]
            return action
        
        
    def feedback(self, state, action, r, memory):
        if memory == 1:
            self.memory1.append([state, action, r])
        else:
            self.memory2.append([state, action, r])

    
    def eval(self):
        Q = 0
        G = 0
        gamma = 0.9

        for m in self.memory1[::-1]:
            s, a, r = m
            vn = max(self.vct[s], 1)  # 当前状态的访问次数
            qn = max(self.qct[(s,a)], 1)  # 当前状态的访问次数

            # update Value
            G = gamma * G + r
            self.v[s] = \
            (self.v[s] * (vn / (vn + 1)))\
            + (G / vn + 1) 

            # update Q
            Q = gamma * Q + r
            # self.q[(s,a)] = \
            # (self.q[(s,a)] * (qn / (qn+1)))\
            # + (Q / qn+1)
            self.q[(s,a)] = self.q[(s,a)] * 0.9 + Q

            self.e_greedy(s)

            self.vct[s] += 1  # 增加访问次数
            self.qct[(s,a)] += 1
        
        self.memory1 = []
        
        Q = 0
        G = 0
        gamma = 0.9

        for m in self.memory2[::-1]:
            s, a, r = m
            vn = max(self.vct[s], 1)  # 当前状态的访问次数
            qn = max(self.qct[(s,a)], 1)  # 当前状态的访问次数

            # update Value
            G = gamma * G + r
            self.v[s] = \
            (self.v[s] * (vn / (vn + 1)))\
            + (G / vn + 1) 

            # update Q
            Q = gamma * Q + r
            # self.q[(s,a)] = \
            # (self.q[(s,a)] * (qn / (qn+1)))\
            # + (Q / qn+1)
            self.q[(s,a)] = self.q[(s,a)] * 0.7 + Q

            self.e_greedy(s)

            self.vct[s] += 1  # 增加访问次数
            self.qct[(s,a)] += 1
        
        self.memory2 = []
    

    def get_qv(self):
        return self.q.copy(), self.qct.copy()
    
    def mix_q(self,q,qct):
        # mix avg 
        # c = a * n/(n+j) + b * j/(n+j)
        for k,v in q.items():
            a = v
            b = q[k]
            n = self.qct[k]
            j = qct[k]
            nj = n + j
            if nj == 0:
                return 
            self.q[k] = a * (n/nj) + b * (j/nj)

    def overwrite_q(self,q):
        self.q = q
    
    def save(self, file = "Agent_weights"):
        json.dump


