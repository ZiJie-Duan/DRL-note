
class OXGame2:

    def __init__(self, w=3, h=3) -> None:
        self.none = 0
        self.o_chess = 1
        self.x_chess = 2
        self.board = [self.none for _ in range(w * h)]

    def init_game(self):
        self.board = [self.none for _ in range(len(self.board))]

    def move_check(self, loc):
        if self.board[loc-1] != self.none:
            return False
        else:
            return True
    
    def winner_check(self):
        # Check rows and columns
        map = [
            [1,4,7],
            [2,5,8],
            [3,6,9],
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [1,5,9],
            [3,5,7]
        ]

        for m in map:
            s = set([self.board[i-1] for i in m])
            if s == set([self.o_chess]):
                return self.o_chess
            if s == set([self.x_chess]):
                return self.x_chess
            
        if 0 in self.board:
            return False
        else:
            return self.x_chess + self.o_chess
    
    def pre_winner_check(self, chess): 
        # Check rows and columns
        map = [
            [1,4,7],
            [2,5,8],
            [3,6,9],
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [1,5,9],
            [3,5,7]
        ]

        for m in map:
            s = [self.board[i-1] for i in m]
            if len(set(s)) == 2:
                if self.none in set(s) and chess in set(s):
                    if s.count(chess) == 2:
                        return True 
    
    def b2s(self):
        return "".join([str(c) for c in self.board])

    def move(self, loc, chess):
        # return [s,a,r,s',end]
        s = self.b2s()
        a = loc
        r = 0
        sd = None
        end = False

        if not self.move_check(loc):
            return [s,a,-1,s,end]
        
        self.board[loc-1] = chess
        sd = self.b2s()

        game_state = self.winner_check()
        pre_win_state = self.pre_winner_check(
            self.o_chess if chess == self.x_chess else self.x_chess)

        if game_state:            
            end = True
            if game_state == chess:
                r = 1.5
            elif game_state == self.o_chess + self.x_chess:
                r = -0.5
            else:
                raise TypeError("Logic Error")
        
        # if pre_win_state:
        #     r = -1.5     
        
        return [s,a,r,sd,end]
    
    def o_move(self, loc):
        return self.move(loc, self.o_chess)
            
    def x_move(self, loc):
        return self.move(loc, self.x_chess)


    def pprint(self, s, a, r, sd, end):

        flag = True if s != sd else False

        print("\n----------------------------")
        print(f"Action_Success: {flag}")
        if flag:
            print(f"Last_Chess: {sd[a-1]}")
            print(f"Last_Step: {a}")
            print(f"Reward: {r}")
            print(f"Game_End: {end}")
            print("- - - - -")
            for row in [sd[i:i+3] for i in range(0, len(sd), 3)]:
                print("| ", end="")
                for cell in row:
                    print(cell, end=" ")
                print("|")
            print("- - - - -")
        else :
            print(f"Reward: {r}")
        print("----------------------------\n")

    def get_board_state(self):
        return self.b2s()