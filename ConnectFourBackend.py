import numpy as np
import pygame
import math
import sys








class Game():
    def __init__(self,debug=False):
        self.board = np.zeros((12,7))
        self.over = False
        self.tie = False
        self.playerlist = [Player('Player 1'),Player('Player 2')]
        self.player_colors = [(255,64,64),(255,215,0)]
        self.squaresize = 75
        self.boardx = 137.5
        self.boardy = 75
        self.turn = np.random.randint(0,2)
        self.preferred_choice = np.random.randint(0,7)
        self.state = 'Title'

     
    def valid_move(self,column):
        return self.board[0][column]==0 and self.board[1][column]==0
     
    def next_open_row(self,column):
        valid_row = 0
        other_piece = False
        r = 0
        while other_piece==False:
            if self.board[r][column]==1:
                valid_row = 2*(int(r/2)-1) + self.turn
                other_piece = True
            elif r == len(self.board)-1:
                valid_row = 2*int(r/2) + self.turn
                other_piece = True
            else:
                r += 1
        return valid_row

     
    def is_gameover(self,row,column):    
        left_pieces = 0
        right_pieces = 0
        down_pieces = 0
        upper_left_pieces = 0
        upper_right_pieces = 0
        lower_left_pieces = 0
        lower_right_pieces = 0
        ul_done = False
        ur_done = False
        ll_done = False
        lr_done = False
        l_done = False
        r_done = False
        

        for c in range(3):

            if 0<=(column-(c+1)):
                if self.board[row][column-(c+1)]==1 and l_done==False:
                    left_pieces += 1
                elif self.board[row][column-(c+1)]==0:
                    l_done = True

            if (column+(c+1))<self.board.shape[1]:
                if self.board[row][column+(c+1)]==1 and r_done==False:
                    right_pieces += 1
                elif self.board[row][column+(c+1)]==0:
                    r_done = True

            if 0<=(column-(c+1)) and 0<=(row-2*(c+1)):
                if self.board[row-2*(c+1)][column-(c+1)]==1 and ul_done==False:
                    upper_left_pieces += 1
                elif self.board[row-2*(c+1)][column-(c+1)]==0:
                    ul_done = True

            if 0<=(column-(c+1)) and (row+2*(c+1))<self.board.shape[0]:
                if self.board[row+2*(c+1)][column-(c+1)]==1 and ll_done==False:
                    lower_left_pieces +=1
                elif self.board[row+2*(c+1)][column-(c+1)]==0:
                    ll_done = True

            if (column+(c+1))<self.board.shape[1] and 0<=(row-2*(c+1)):
                if self.board[row-2*(c+1)][column+(c+1)]==1 and ur_done==False:
                    upper_right_pieces += 1
                elif self.board[row-2*(c+1)][column+(c+1)]==0:
                    ur_done = True


            if (column+(c+1))<self.board.shape[1] and (row+2*(c+1))<self.board.shape[0]:
                if self.board[row+2*(c+1)][column+(c+1)]==1 and lr_done==False:
                    lower_right_pieces += 1
                elif self.board[row+2*(c+1)][column+(c+1)]==0:
                    lr_done = True



        
        if (right_pieces + left_pieces >= 3):
            self.over=True
            return
        else:
            for down_counter,row_number in enumerate(self.board[row+2:,column]):
                if down_counter%2==0:
                    
                    if row_number==0:
                        break
                    else:
                        down_pieces+=1
                        continue
                elif down_counter==1:
                    continue
                down_counter+=(down_counter + 1)%2
            
            if (down_pieces>=3):
                self.over=True
                return


        if (lower_right_pieces + upper_left_pieces)>=3 or (upper_right_pieces + lower_left_pieces)>=3:
            self.over=True

        else:
            self.over=False



        return


    def is_tie(self):
        open_moves = 0
        for c in range(self.board.shape[1]):
            if self.valid_move(c)==True:
                open_moves += 1
        if open_moves==0:
            self.over =True
            self.tie = True
        return

            
    def drop_piece(self,row,column):
        self.board[row][column] = 1


    def draw_board(self,screen):
        for r in range(len(self.board)):
            for c in range(len(self.board[1])):
                if self.board[r][c]==1:
                    pygame.draw.circle(screen,self.player_colors[int(r%2)],((int(c*self.squaresize+self.boardx + self.squaresize*0.5)),(int(int(r/2)*self.squaresize + self.boardy + self.squaresize*0.5))),int(self.squaresize*0.4+1))
                    pygame.draw.circle(screen,self.player_colors[int(r%2)],((int(c*self.squaresize+self.boardx + self.squaresize*0.5)),(int(int(r/2)*self.squaresize + self.boardy + self.squaresize*0.5))),int(self.squaresize*0.4))
                elif r%2==0 and self.board[r+1][c]==0:
                    pygame.draw.circle(screen,(0,0,0),((int(c*self.squaresize+self.boardx + self.squaresize*0.5)),(int(int(r/2)*self.squaresize + self.boardy + self.squaresize*0.5))),int(self.squaresize*0.4+1))

    def player_choice(self,screen,x,y):
        pygame.draw.circle(screen,(0,0,0),((int(x*self.squaresize+self.boardx + self.squaresize*0.5)),int((self.boardy - self.squaresize*0.5))),int(self.squaresize*0.4)+1)
        pygame.draw.circle(screen,self.player_colors[self.turn],((int(x*self.squaresize+self.boardx + self.squaresize*0.5)),int((self.boardy - self.squaresize*0.5))),int(self.squaresize*0.4))


    def evaluate_board(self,state):
        value = 0
          
        for r in range(state.shape[0]):
            if r%2==0:
                #horizontal counting
                for c in range(state.shape[1]-3):
                    if np.sum(state[r][c:c+4])==4:
                        value = 1000
                        return value
                    elif np.sum(state[r][c:c+4])==3 and np.sum(state[r+1][c:c+4])==0:
                        value += 5
                    elif np.sum(state[r][c:c+4])==2 and np.sum(state[r+1][c:c+4])==0:
                        value += 2
            else:
                for c in range(state.shape[1]-3):
                    if np.sum(state[r][c:c+4])==4:
                        value = -1000
                        return value
                    elif np.sum(state[r][c:c+4])==3 and np.sum(state[r-1][c:c+4])==0:
                        value -= 5
                    elif np.sum(state[r][c:c+4])==2 and np.sum(state[r-1][c:c+4])==0:
                        value -= 2
                        
        for c in range(state.shape[1]):
            for r in range(state.shape[0]-6):
                if r%2==0:
                    #vertical counting with center column factored in
                    num_player = 0
                    num_opp = 0
                    for index,piece in enumerate(state[r:r+6][c]):
                        if index%2==0 and piece==1:
                            num_player += 1
                        if index%2==1 and piece==1:
                            num_opp += 1
                    if num_player==4:
                        value = 1000
                        return value
                    elif num_opp>0:
                        value = value
                    elif num_player==3 and c==3:
                        value += 8
                    elif num_player==3:
                        value += 5
                    elif num_player==2 and c==3:
                        value += 4
                    elif num_player==2:
                        value += 2
                else:
                    num_player = 0
                    num_opp = 0
                    for index,piece in enumerate(state[r:r+6][c]):
                        if index%2==0 and piece==1:
                            num_player += 1
                        if index%2==1 and piece==1:
                            num_opp += 1
                    if num_player==4:
                        value = -1000
                        return value
                    elif num_opp>0:
                        value = value
                    elif num_player==3 and c==3:
                        value -= 8
                    elif num_player==3:
                        value -= 5
                    elif num_player==2 and c==3:
                        value -= 4
                    elif num_player==2:
                        value -= 2                
                        
        for r in range(state.shape[0]-6):
            for c in range(state.shape[1]-3):
                #upper right diagonal counting
                num_opp = 0
                num_player = 0
                if r%2==0:
                    for piece in [state[r+(2*i)][c+i] for i in range(4)]:
                        num_player += piece
                    for piece in [state[r+(2*i)+1][c+i] for i in range(4)]:
                        num_opp += piece
                        
                    if num_player==4:
                        value = 1000
                        return value
                    elif num_opp>0:
                        value = value
                    elif num_player==3:
                        value += 5
                    elif num_player==2:
                        value += 2
                    elif num_opp==4:
                        value = -1000
                        return value
                    elif num_player>0:
                        value = value
                    elif num_opp==3:
                        value -= 5
                    elif num_opp==2:
                        value -= 2
                        
        for r in range(state.shape[0]-6):
            for c in range(state.shape[1]-3):
                #upper left diagonal counting
                num_opp = 0
                num_player = 0
                if r%2==0:
                    for piece in [state[r+(2*i)][c-i] for i in range(4)]:
                        num_player += piece
                    for piece in [state[r+(2*i)+1][c-i] for i in range(4)]:
                        num_opp += piece
                        
                    if num_player==4:
                        value = 1000
                        return value
                    elif num_opp>0:
                        value = value
                    elif num_player==3:
                        value += 5
                    elif num_player==2:
                        value += 2
                    elif num_opp==4:
                        value = -1000
                        return value
                    elif num_player>0:
                        value = value
                    elif num_opp==3:
                        value -= 5
                    elif num_opp==2:
                        value -= 2
        
        return value




class Player():
    def __init__(self,name,debug=False):
        self.name = name
        self.human = True
        self.model = 'Human'
        self.winner = False

    def swap_colors(board):
        board[[0,1,2,3,4,5,6,7,8,9,10,11]] = board[[1,0,3,2,5,4,7,6,9,8,11,10]]



