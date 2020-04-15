import copy
import os
from os import path
from collections import deque
import math
import random
import pygame

import numpy as np
import pandas as pd
import cv2
from PIL import Image
import pickle

import torch
from torch.utils.data import Dataset, DataLoader


from C4Backend import Game, Player
from C4Net import C4Net, ImageDataset
from MCTS import MCTS



MIN_GAMES = 100
MAX_MEM_LEN = 10000
MIN_TRAINS = 10
BATCH_SIZE = 256
MINIBATCH_SIZE = 64
EVAL_GAMES = 40
WATCH_MOVES = False
CURRENT_DIR = path.abspath(path.curdir)


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

screen.blit(background,(0,0))
screen.blit(table,(0,int(display_height*0.55)))


agent = C4Net()
best_player = C4Net()

latest_version = np.max(np.array([int(model.split(' ')[1]) for model in os.listdir(CURRENT_DIR + '/Models/Versions/')]))

if latest_version==0:
    torch.save(best_player.state_dict(),CURRENT_DIR + f'/Models/Best Model')

agent.load_state_dict(torch.load(CURRENT_DIR + f'/Models/Versions/Model {latest_version}'))
best_player.load_state_dict(torch.load(CURRENT_DIR + '/Models/Best Model'))



memory = deque([], maxlen=MAX_MEM_LEN)
game_counter = 0
train_counter = 0
model_counter = latest_version + 1

training = True

while training:
            
    game = Game()
    trainexamples = []

    if WATCH_MOVES:
        pygame.draw.rect(screen,black,(board_x-1,board_y-1,NUM_COLS*SQUARE_SIZE+2,NUM_ROWS*SQUARE_SIZE+2))
        pygame.draw.rect(screen,blue,board_dim)
        game.draw_board(screen,False,game.board)


    while not game.over:


        mcts = MCTS(agent,game,screen,100)
        pi = mcts.get_action_prop()
        action = np.random.choice(7,p=pi)
        pi = torch.tensor(pi)
        row = game.next_open_row(game.board,action)
        game.drop_piece(row,action,game.turn+1)
        vision = game.render_vision(screen)

        if WATCH_MOVES:
            game.draw_board(screen,False,game.board)
            pygame.display.flip()

        trainexamples.append([vision,game.turn,pi,None])
        if game.is_gameover(game.board,row,action,game.turn+1):
            game.over = True
            
            for x in trainexamples:
                memory.append([x[0],x[2],(-1)**(x[1]!=game.turn)])
            # memory.append([(x[0],x[2],(-1)**(x[1]!=game.turn)) for x in trainexamples])


        elif game.is_tie(game.board):
            game.over = True
            for x in trainexamples:
                memory.append([x[0],x[2],0])
        else:
            game.turn = (game.turn+1)%2

    game_counter += 1

    print(f'game {game_counter} finished')

    if game_counter%MIN_GAMES==0:

        # print('train network')

        batch = random.sample(list(memory),BATCH_SIZE)


        dataset = ImageDataset(batch)
        dataloader = DataLoader(
                        dataset, 
                        batch_size=MINIBATCH_SIZE,
                        shuffle=True
                        )

        for data in dataloader:

            input_vision, target_pi, target_v = data
            output_pi, output_v = agent.predict(input_vision.float())


            l_pi = torch.sum(output_pi*target_pi)/target_pi.size()[0]
            l_v = torch.sum((target_v-output_v.view(-1))**2)/target_v.size()[0]
            total_loss = l_pi + l_v

            print(f'loss was {total_loss}')

            optimizer = torch.optim.Adam(agent.parameters())


            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()


        train_counter += 1

        print(f'batch {train_counter} trained')


        if train_counter%MIN_TRAINS==0:

            best_player_wins = 0
            agent_wins = 0

            for g in range(EVAL_GAMES):

                game = Game()

                game.turn = g%2

                while not game.over:

                    if game.turn==0:
                        mcts = MCTS(best_player,game,screen,100)
                    else:
                        mcts = MCTS(agent,game,screen,100)

                    pi = mcts.get_action_prop()
                    action = np.argmax(pi)
                    pi = torch.tensor(pi)
                    row = game.next_open_row(game.board,action)
                    game.drop_piece(row,action,game.turn+1)

                    if WATCH_MOVES:
                        game.draw_board(screen,False,game.board)
                        pygame.display.flip()

                    if game.is_gameover(game.board,row,action,game.turn+1):
                        game.over = True
                        if game.turn==0:
                            best_player_wins += 1
                        else:
                            agent_wins += 1
                    
                    elif game.is_tie(game.board):
                        game.over = True


                    else:
                        game.turn = (game.turn+1)%2                

            win_percent = (agent_wins)/(agent_wins + best_player_wins)

            print(f'agent won {int(win_percent*100)}% of games')

            if win_percent>=0.55:

                torch.save(best_player.state_dict(),CURRENT_DIR + f'/Models/Versions/Model {model_counter}')
                torch.save(agent.state_dict(),CURRENT_DIR + f'/Models/Best Model')

                model_counter += 1
            
            else:
                pass
        

    

