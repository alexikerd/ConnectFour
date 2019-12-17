import numpy as np
import pygame
import math
import sys
import time
import threading
import copy

display_width = 800
display_height = 600





class Game():
    def __init__(self,debug=False):
        self.board = np.zeros((6,7))
        self.over = False
        self.tie = False
        self.playerlist = [Player('Player 1'),Player('Player 2')]
        self.player_colors = [(0,0,0),(255,64,64),(255,215,0)]
        self.squaresize = 75
        self.boardx = 137.5
        self.boardy = 75
        self.turn = np.random.randint(0,2)
        self.preferred_choice = 4
        self.display = 'Title'
        self.startcheck = [False,False]
        self.editor = 0
        self.editingtext = False
        self.score = [0,0]

     
    def valid_move(self,state,column):
        return state[0][column]==0
     
    def next_open_row(self,state,column):
        for r in reversed(range(state.shape[0])):
            if state[r][column]==0:
                return r
            else:
                continue


     
    def is_gameover(self,state,row,column,piece):    
        num_horiz = 0
        num_ul = 0
        num_ur = 0



        for r in range(3):
            if (row+1+r)==state.shape[0] or state[row+r+1][column]!=piece:
                break
            elif r==2:
                return True
            else:
                continue

        for c in range(3):
            if 0>(column-(c+1)) or state[row][column-(c+1)]!=piece:
                break
            elif c==2:
                return True
            else:
                num_horiz+=1
                continue

        for c in range(3):
            if num_horiz==3:
                return True
            elif (column+(c+1))==state.shape[1] or state[row][column+(c+1)]!=piece:
                break
            elif c==2:
                return True
            else:
                num_horiz+=1
                continue


        for c in range(3):
            if 0>(column-(c+1)) or 0>(row-(c+1)) or state[row-(c+1)][column-(c+1)]!=piece:
                break
            elif c==2:
                return True
            else:
                num_ul+=1
                continue

        for c in range(3):
            if num_ul==3:
                return True
            elif (column+(c+1))==state.shape[1] or (row+(c+1))==state.shape[0] or state[row+(c+1)][column+(c+1)]!=piece:
                break
            elif c==2:
                return True
            else:
                num_ul+=1
                continue 

        for c in range(3):
            if 0>(column-(c+1)) or (row+(c+1))==state.shape[0] or state[row+(c+1)][column-(c+1)]!=piece:
                break
            elif c==2:
                return True
            else:
                num_ur+=1
                continue

        for c in range(3):
            if num_ur==3:
                return True
            elif (column+(c+1))==state.shape[1] or 0>(row-(c+1)) or state[row-(c+1)][column+(c+1)]!=piece:
                break
            elif c==2:
                return True
            else:
                num_ur+=1
                continue




        

    def is_tie(self,state):
        open_moves = 0
        for c in range(state.shape[1]):
            if self.valid_move(state,c)==True:
                open_moves += 1
        if open_moves==0:
            return True
        else:
            return False
            
    def drop_piece(self,row,column,piece): 
        self.board[row][column] = piece


    def draw_board(self,screen):
        for r in range(self.board.shape[0]):
            for c in range(self.board.shape[1]):
                pygame.draw.circle(screen,(0,0,0),((int(c*self.squaresize+self.boardx + self.squaresize*0.5)),(int(int(r)*self.squaresize + self.boardy + self.squaresize*0.5))),int(self.squaresize*0.4+1))
                pygame.draw.circle(screen,self.player_colors[int(self.board[r][c])],((int(c*self.squaresize+self.boardx + self.squaresize*0.5)),(int(int(r)*self.squaresize + self.boardy + self.squaresize*0.5))),int(self.squaresize*0.4))


    def player_choice(self,screen,x,y):
        pygame.draw.circle(screen,(0,0,0),((int(x*self.squaresize+self.boardx + self.squaresize*0.5)),int((self.boardy - self.squaresize*0.5))),int(self.squaresize*0.4)+1)
        pygame.draw.circle(screen,self.player_colors[self.turn+1],((int(x*self.squaresize+self.boardx + self.squaresize*0.5)),int((self.boardy - self.squaresize*0.5))),int(self.squaresize*0.4))


    def evaluate_board(self,board,piece,minimatrix):
        value = 0

                 #horizontal counting         
        for r in range(board.shape[0]):
            for c in range(board.shape[1]-3):
                unique_piece, counts = np.unique(board[r,c:c+4],return_counts=True)
                if counts[np.where(unique_piece==piece)[0]].size==0:
                    num_1 = 0
                else:
                    num_1 = counts[np.where(unique_piece==piece)[0]]

                if counts[np.where(unique_piece==(piece%2 + 1))[0]].size==0:
                    num_2 = 0
                else:
                    num_2 = counts[np.where(unique_piece==(piece%2 + 1))[0]]

                if (num_1>0 and num_2>0) or (num_1 + num_2)==0:
                    value = value
                elif num_1==4:
                    value = minimatrix[3]
                    return value
                elif num_1==3:
                    value += minimatrix[2]                   
                elif num_1==2:
                    value += minimatrix[1]
                elif num_2==4:
                    value = -minimatrix[3]
                    return value
                elif num_2==3:
                    value -= minimatrix[2]
                elif num_2==2:
                    value -= minimatrix[1]


                #vertical counting   
        for r in range(board.shape[0]-3):
            for c in range(board.shape[1]):
                unique_piece, counts = np.unique(board[r:r+4,c],return_counts=True)
                if counts[np.where(unique_piece==piece)[0]].size==0:
                    num_1 = 0
                else:
                    num_1 = counts[np.where(unique_piece==piece)[0]]

                if counts[np.where(unique_piece==(piece%2 + 1))[0]].size==0:
                    num_2 = 0
                else:
                    num_2 = counts[np.where(unique_piece==(piece%2 + 1))[0]]

                if (num_1>0 and num_2>0) or (num_1 + num_2)==0:
                    value = value
                elif num_1==4:
                    value = minimatrix[3]
                    return value
                elif num_1==3:
                    value += minimatrix[2]
                elif num_1==2:
                    value += minimatrix[1]
                elif num_2==4:
                    value = -minimatrix[3]
                    return value
                elif num_2==3:
                    value -= minimatrix[2]
                elif num_2==2:
                    value -= minimatrix[1]


     
#upper right diagonal counting

        for r in range(board.shape[0]-3):
            for c in range(board.shape[1]-3):
                unique_piece, counts = np.unique(np.diagonal(np.fliplr(board[r:r+4,c:c+4])),return_counts=True)    
                if counts[np.where(unique_piece==piece)[0]].size==0:
                    num_1 = 0
                else:
                    num_1 = counts[np.where(unique_piece==piece)[0]]

                if counts[np.where(unique_piece==(piece%2 + 1))[0]].size==0:
                    num_2 = 0
                else:
                    num_2 = counts[np.where(unique_piece==(piece%2 + 1))[0]]

                if (num_1>0 and num_2>0) or (num_1 + num_2)==0:
                    value = value
                elif num_1==4:
                    value = minimatrix[3]
                    return value
                elif num_1==3:
                    value += minimatrix[2]
                elif num_1==2:
                    value += minimatrix[1]
                elif num_2==4:
                    value = -minimatrix[3]
                    return value
                elif num_2==3:
                    value -= minimatrix[2]
                elif num_2==2:
                    value -= minimatrix[1]        


                            
    #upper left diagonal counting
        
        for r in range(board.shape[0]-3):
            for c in range(board.shape[1]-3):
                unique_piece, counts = np.unique(np.diagonal(board[r:r+4,c:c+4]),return_counts=True)    
                if counts[np.where(unique_piece==piece)[0]].size==0:
                    num_1 = 0
                else:
                    num_1 = counts[np.where(unique_piece==piece)[0]]

                if counts[np.where(unique_piece==(piece%2 + 1))[0]].size==0:
                    num_2 = 0
                else:
                    num_2 = counts[np.where(unique_piece==(piece%2 + 1))[0]]

                if (num_1>0 and num_2>0) or (num_1 + num_2)==0:
                    value = value
                elif num_1==4:
                    value = minimatrix[3]
                    return value
                elif num_1==3:
                    value += minimatrix[2]
                elif num_1==2:
                    value += minimatrix[1]
                elif num_2==4:
                    value = -minimatrix[3]
                    return value
                elif num_2==3:
                    value -= minimatrix[2]
                elif num_2==2:
                    value -= minimatrix[1]        


            #center counting
        for r in range(board.shape[0]):
            if board[r][3]==piece:
                value += minimatrix[0]
            elif board[r][3]==(piece%2 + 1):
                value -= minimatrix[0]
            else:
                value = value



        return value


    def minimax(self, node, depth, current_turn, piece, alpha, beta, minimatrix):
        if depth==0:
            return self.evaluate_board(node,(self.turn)+1,minimatrix)

        elif self.is_tie(node)==True:
            return 0
        else:
            if current_turn==0: #maximizing
                value = -math.inf
                for c in range(node.shape[1]):

                    if node[0][c]==0:
                        child = node.copy()
                        valid_row = Game().next_open_row(node,c)
                        child[valid_row][c] = piece
                        if Game().is_gameover(child,valid_row,c,piece)==True:
                            return self.evaluate_board(child,(self.turn)+1,minimatrix)
                        value = max(value, self.minimax(child, depth-1, (current_turn+1)%2,(piece)%2+1,alpha,beta,minimatrix))
                        alpha = max(alpha,value)
                    if alpha>=beta:
                        break
                return value


            else: #minimizing
                value = math.inf
                for c in range(node.shape[1]):
                    if node[0][c]==0:
                        child = node.copy()
                        valid_row = Game().next_open_row(node,c)
                        child[valid_row][c] = piece
                        if Game().is_gameover(child,valid_row,c,piece)==True:
                            return self.evaluate_board(child,(self.turn)+1,minimatrix)
                        value = min(value, self.minimax(child, depth-1, (current_turn+1)%2,(piece)%2+1,alpha,beta,minimatrix))
                        beta = min(beta,value)
                    if alpha>=beta:
                        break
                return value



    def simpmax(self, node, depth, current_turn, piece, alpha, beta, minimatrix): #There is an error with determining values
        if depth==0:
            return 0

        elif self.is_tie(node)==True:
            return 0
        else:
            if current_turn==0: #maximizing
                value = -math.inf
                for c in range(node.shape[1]):
                    if node[0][c]==0:
                        child = node.copy()
                        valid_row = Game().next_open_row(node,c)
                        child[valid_row][c] = piece
                        if Game().is_gameover(child,valid_row,c,piece)==True:
                            return 100
                        value = max(value, self.simpmax(child, depth-1, (current_turn+1)%2,(piece)%2+1,alpha,beta,minimatrix))
                        alpha = max(alpha,value)
                    if alpha>=beta:
                        break
                return value



            else: #minimizing
                value = math.inf
                for c in range(node.shape[1]):
                    if node[0][c]==0:
                        child = node.copy()
                        valid_row = Game().next_open_row(node,c)
                        child[valid_row][c] = piece
                        if Game().is_gameover(child,valid_row,c,piece)==True:
                            return -100
                        value = min(value, self.simpmax(child, depth-1, (current_turn+1)%2,(piece)%2+1,alpha,beta,minimatrix))
                        beta = min(beta,value)
                    if alpha>=beta:
                        break
                return value


 












class Player():
    def __init__(self,name,debug=False):
        self.name = name
        self.human = True
        self.model = 'Human'
        self.winner = False
        self.depth = 1
        self.thinking = [False,False,False]
        self.minimatrix = [1,2,5,1000]
        self.fitness = 0

    def determine_preference(self,state,turn,piece,game):
        if self.model=='Human':
            return

        if self.depth==1:
            minimatrix = [2, 49, 198, 1000]

        elif self.depth==3:
            minimatrix = [20, 160, 241, 999]
        
        elif self.depth==5:
            minimatrix = [1, 120, 316, 1000]

        else:
            minimatrix = [0,0,0,0]

        node = state.copy()

        current_turn = 0

        if self.model=='Random':
            choice = np.random.randint(0,state.shape[1])
            while game.valid_move(state,choice)==False:
                choice = np.random.randint(0,state.shape[1])
            return choice

        if self.model=='Minimax':
            value = -math.inf
            best_column = []
            for c in range(state.shape[1]):
                if game.valid_move(node,c)==True:

                    child = node.copy()
                    valid_row = game.next_open_row(child,c)
                    child[valid_row][c] = piece
                    if game.is_gameover(child,valid_row,c,piece)==True:
                        current_value = math.inf
                    else:
                        current_value = game.minimax(child,self.depth-1,(current_turn+1)%2,(piece)%2+1,-math.inf,math.inf,minimatrix)
                    # print(f'{c}  {current_value}')                    
                    if current_value>value:
                        value = current_value
                        best_column = []
                        best_column.append(c)
                    elif current_value==value:
                        best_column.append(c)
                    else:
                        continue
                else:
                    continue
            return best_column[np.random.randint(len(best_column))]


        if self.model=='Simplemax':
            value = -math.inf
            best_column = []
            for c in range(state.shape[1]):
                if game.valid_move(node,c)==True:
                    child = node.copy()
                    valid_row = game.next_open_row(child,c)
                    child[valid_row][c] = piece
                    if game.is_gameover(child,valid_row,c,piece)==True:
                        current_value = 100
                    else:
                        current_value = game.simpmax(child,self.depth+3,(current_turn+1)%2,(piece)%2+1,-math.inf,math.inf,minimatrix)
                    # print(f'{c}  {current_value}')
                    if current_value>value:
                        value = current_value
                        best_column = []
                        best_column.append(c)
                    elif current_value==value:
                        best_column.append(c)
                    else:
                        continue
                else:
                    continue
            return best_column[np.random.randint(len(best_column))]
                    



class Button():

    def __init__(self,x,y,fontsize,text,color):
        self.x = x
        self.y = y
        self.fontsize = fontsize
        self.text = text
        self.color = color
        self.buttoncolor = (255,255,255)
        self.font = pygame.font.SysFont('Comic Sans MS',self.fontsize)
        self.fontwidth, self.fontheight = self.font.size(self.text)
        self.presscheck = [False,False]
        self.customized = False


    def draw_button(self,screen,mousex,mousey):

        for fs in reversed(range(self.fontsize)):
            font = pygame.font.SysFont('Comic Sans MS',fs)
            fontwidth,fontheight = font.size(self.text)
            if fontwidth<self.fontwidth:
                if self.x-5<=mousex<=self.x+self.fontwidth+5 and self.y<=mousey<=self.y+self.fontheight:

                    pygame.draw.rect(screen,self.buttoncolor,(self.x-5,self.y,self.fontwidth+10,self.fontheight)) 
                    text = font.render(self.text,False,self.color)
                    screen.blit(text,(self.x,self.y + (self.fontheight - fontheight)))

                else:

                    pygame.draw.rect(screen,self.color,(self.x-5,self.y,self.fontwidth+10,self.fontheight)) 
                    text = font.render(self.text,False,self.buttoncolor)
                    screen.blit(text,(self.x,self.y + (self.fontheight - fontheight)))
                break


    def get_coordinates(self):

        return self.x-5,self.x+self.fontwidth+5,self.y,self.y+self.fontheight

    def got_pressed(self,click,mousex,mousey):

        start_x1, start_x2, start_y1, start_y2 = self.get_coordinates()   

        if (click==0 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2) or self.presscheck[0]==True:

            if (click==1 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2) or self.presscheck[1]==True:

                if (click==0 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2):
                    self.presscheck = [False,False]
                    return True
                elif (click==1 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2):
                    self.presscheck[1] = True
                else:
                    self.presscheck = [False,False]
            elif click==0 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2:
                self.presscheck[0] = True
            else:
                self.presscheck[0] = False

        return False






class Menu_Piece():
    def __init__(self,color,x,colorwheel):
        self.x = x
        self.y = 218
        self.radius = 17
        self.color = color
        self.colorwheel = colorwheel
        self.presscheck = [False,False]


    def draw(self,screen):
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.radius+1)
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

    def got_pressed(self,click,mousex,mousey):

        startx, starty, startr = self.get_coordinates()   

        if (click==0 and (math.sqrt((startx-mousex)**2 + (starty-mousey)**2))<=startr) or self.presscheck[0]==True:

            if (click==1 and (math.sqrt((startx-mousex)**2 + (starty-mousey)**2))<=startr) or self.presscheck[1]==True:

                if (click==0 and (math.sqrt((startx-mousex)**2 + (starty-mousey)**2))<=startr):
                    self.presscheck = [False,False]
                    return True
                elif (click==1 and (math.sqrt((startx-mousex)**2 + (starty-mousey)**2))<=startr):
                    self.presscheck[1] = True
                else:
                    self.presscheck = [False,False]
            elif click==0 and (math.sqrt((startx-mousex)**2 + (starty-mousey)**2))<=startr:
                self.presscheck[0] = True
            else:
                self.presscheck[0] = False
        return False


    def get_coordinates(self):

        return self.x,self.y, self.radius


class Key():

    def __init__(self,x,y,fontsize,text,color,keynumber):
        self.x = x
        self.y = y
        self.fontsize = fontsize
        self.text = text
        self.color = color
        self.buttoncolor = (255,255,255)
        self.font = pygame.font.SysFont('Comic Sans MS',self.fontsize)
        self.fontwidth, self.fontheight = self.font.size(self.text)
        self.keynumber = keynumber
        self.pressed = False

    def draw_key(self,screen):

        if self.pressed==True:
            pygame.draw.rect(screen,self.buttoncolor,(self.x-5,self.y,self.fontwidth+10,self.fontheight)) 
            text = self.font.render(self.text,False,self.color)
            screen.blit(text,(self.x,self.y))
            self.pressed = True

        else:

            pygame.draw.rect(screen,self.color,(self.x-5,self.y,self.fontwidth+10,self.fontheight)) 
            text = self.font.render(self.text,False,self.buttoncolor)
            screen.blit(text,(self.x,self.y))






class Cloud():
    def __init__(self):
        self.velocity = -1
        self.x = display_width + 50
        self.y = np.random.randint(-int(display_height/4),int(display_height*7/24))
        self.width = np.random.randint(int(display_width/8),int(display_width/2))
        self.height = np.random.randint(int(display_height/10),int(display_height/2) - self.y - 50)

    def move(self):
        self.x += self.velocity

    def draw(self,screen):
        cloud = pygame.transform.scale(pygame.image.load('Graphics/Cloud.png'),(self.width,self.height))
        screen.blit(cloud,(self.x,self.y))



class Text_Editor():
    def __init__(self,cursor):
        self.cursor = cursor


    def create_string(self):
        return self.cursor

    def add_letter(self,string,letter):
        if len(string)==8:
            return string
        else:
            temp_list = list(string)
            x = string.index('|')
            final_list = temp_list[:x] + list(letter) + temp_list[x:]
            return "".join(final_list)

    def delete_letter(self,string):
        temp_list = list(string)
        x = string.index('|')
        final_list = temp_list[:x-1] + temp_list[x:]
        return "".join(final_list)

    def move_left(self,string):
        temp_list = list(string)
        x = string.index('|')
        if x==0:
            return string
        else:
            final_list = temp_list[:x-1] + list(self.cursor) + list(temp_list[x-1]) + temp_list[x+1:]
            return "".join(final_list)

    def move_right(self,string):
        temp_list = list(string)
        x = string.index('|')
        if len(string)==x+1:
            return string
        else:    
            final_list = temp_list[:x] + list(temp_list[x+1]) + list(self.cursor) + temp_list[x+2:]
            return "".join(final_list)



class Future:
    def __init__(self,func,*param):
        self.__done = False
        self.__result = None
        self.__status = 'working'
        self.__C = threading.Condition()
        self.__T = threading.Thread(target=self.Wrapper,args=(func,param))
        self.__T.setName("FutureThread")
        self.__T.start()
        self.done = False

    def repr(self):
        return '<Future at '+hex(id(self))+':'+self.__status+'>'

    def __call__(self):
        self.__C.acquire()
        while self.__done==False:
            self.__C.wait()
        self.__C.release()
        a=copy.deepcopy(self.__result)
        return a

    def Wrapper(self,func,param):
        self.__C.acquire()
        try:
            self.__result=func(*param)
        except:
            self.__result="Exception raised within Future"
        self.__done = True
        self.done = True
        self.__status='self.__result'
        self.__C.notify()
        self.__C.release()


