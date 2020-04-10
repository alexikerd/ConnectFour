import math
import pygame

import numpy as np
import pandas as pd
import cv2
from PIL import Image

import torch
from torch.utils.data import Dataset, DataLoader


from C4Backend import Game, Player
from C4Net import C4Net, ImageDataset


#https://web.stanford.edu/~surag/posts/alphazero.html

NUM_GAMES = 20
ITERATIONS = 25
BATCH_SIZE = 1


pygame.init()

NUM_ROWS = 6
NUM_COLS = 7
display_width = 800
display_height = 600
SQUARE_SIZE = 75
IMG_SIZE = 28
board_x = 137.5
board_y = 75
cloud_x = display_width
cloud_y = display_height/3
board_dim = (board_x,board_y,NUM_COLS*SQUARE_SIZE,NUM_ROWS*SQUARE_SIZE)
blue = (0,0,205)
black = (0,0,0)
white = (255,255,255)
red = (255,64,64)

screen = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load('Graphics/Background.png'),(display_width,int(display_height)))
table = pygame.transform.scale(pygame.image.load('Graphics/Table.png'),(display_width,int(display_height*0.5)))
namefont = pygame.font.SysFont('Comic Sans MS', 30)


game = Game()


moves = []
boards = []
players = []

for _ in range(1):

    screen.blit(background,(0,0))
    screen.blit(table,(0,int(display_height*0.55)))
    move = 1
    while game.over==False:
        valid_move = False
        while valid_move==False:
            column = np.random.randint(0,7)
            valid_move = game.valid_move(game.board,column)
        row = game.next_open_row(game.board,column)
        game.board[row][column] = game.turn + 1
        moves.append(column)
        players.append(game.turn)
        pygame.draw.rect(screen,black,(board_x-1,board_y-1,NUM_COLS*SQUARE_SIZE+2,NUM_ROWS*SQUARE_SIZE+2))
        pygame.draw.rect(screen,blue,board_dim)
        aeyes = screen.copy()
        game.draw_board(aeyes,True,game.board)
        game.draw_board(screen,False,game.board)
        pygame.display.flip()
        pygame.display.update()
        vision_image = game.render_vision(screen)
        image = pygame.surfarray.array3d(aeyes)
        image = np.moveaxis(image,0,1)
        image = image[int(board_y-1):int(board_y+NUM_ROWS*SQUARE_SIZE+1),int(board_x-1):int(board_x+NUM_COLS*SQUARE_SIZE+1)]
        image = cv2.resize(image,(IMG_SIZE,IMG_SIZE))
        # im = Image.fromarray(image)
        # im.save(f'test_{move}.png')
        # pygame.image.save(screen, "screenshot.png")
        image = np.moveaxis(image,-1,0)
        image = torch.tensor(image)

        boards.append(image)


        if game.is_gameover(game.board,row,column,game.turn+1)==True:
            game.over = True
            pygame.quit()
        elif game.is_tie(game.board)==True:
            game.over = True
            pygame.quit()
        else:
            game.turn = (game.turn+1)%2
        move += 1


sample = boards[0].unsqueeze(0)



agent = C4Net()

with torch.no_grad():
    prediction = agent.predict(sample.float())


pi = prediction[0]
q = prediction[1]

test = np.zeros((7))

test[2:4] = 1

print(pi)
print(q)
print(pi*test)





