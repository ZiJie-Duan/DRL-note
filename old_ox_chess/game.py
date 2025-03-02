

class OXGame:

    def __init__(self) -> None:
        self.w = 3
        self.h = 3
        self.none = 0
        self.x_chess = 1
        self.o_chess = 2
        self.board = \
        [[self.none for _ in range(self.w)] for _ in range(self.h)]
        self.last_chess = -1
        self.last_step = (-1,-1)
        self.winner = None
        self.end = False


    def init_game(self):
        self.board = \
        [[self.none for _ in range(self.w)] for _ in range(self.h)]
        self.last_chess = -1
        self.last_step = (-1,-1)
        self.winner = None
        self.end = False

    def move_check(self, x, y):
        if self.board[x][y] != self.none:
            return False
        else:
            return True
    
    def get_state(self, success):
        r = 0
        if self.winner != None and self.winner != 3:
            if self.winner == self.last_chess:
                r = 1
            else:
                r = -1
        if not success:
            r = -1
            
        return (success,    # success flag
                self.board, 
                self.last_chess, 
                self.last_step,
                r,
                self.end)
    
    def winner_check(self):
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != self.none:
                self.winner = self.board[i][0]
                self.end = True
                return self.winner
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != self.none:
                self.winner = self.board[0][i]
                self.end = True
                return self.winner
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != self.none:
            self.winner = self.board[0][0]
            self.end = True
            return self.winner
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != self.none:
            self.winner = self.board[0][2]
            self.end = True
            return self.winner
        
        if all(cell != self.none for row in self.board for cell in row):
            self.winner = 3
            self.end = True
            return self.winner
        
        return None
        

    def x_move(self,x,y):
        if self.winner != None:
            return self.get_state(False)
        
        if self.last_chess == self.x_chess:
            return self.get_state(False)
        
        if not self.move_check(x,y):
            return self.get_state(False)
        
        self.board[x][y] = self.x_chess

        self.last_step = (x,y)
        self.last_chess = self.x_chess

        self.winner_check()
        return self.get_state(True)

    
    def o_move(self,x,y): 
        if self.winner != None:
            return self.get_state(False)
        
        if self.last_chess == self.o_chess:
            return self.get_state(False)
        
        if not self.move_check(x,y):
            return self.get_state(False)
        
        self.board[x][y] = self.o_chess

        self.last_step = (x,y)
        self.last_chess = self.o_chess

        self.winner_check()
        return self.get_state(True)


    def pprint(self, flag, board,
               last_chess, last_step, 
               r, end):
        
        print("\n----------------------------")
        print(f"Action_Success: {flag}")
        if flag:
            print(f"Last_Chess: {last_chess}")
            print(f"Last_Step: {last_step}")
            print(f"Reward: {r}")
            print(f"Game_End: {end}")
            print("- - - - -")
            for row in board:
                print("| ", end="")
                for cell in row:
                    print(cell, end=" ")
                print("|")
            print("- - - - -")
        else :
            print(f"Reward: {r}")
        print("----------------------------\n")
