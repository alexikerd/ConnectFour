import copy
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




class MCTS():

    def __init__(self,nnet,game,screen,sims):

        self.nnet = nnet
        self.Qsa = {}
        self.Nsa = {}
        self.Ns = {}
        self.Ps = {}

        self.Es = {}
        self.Vs = {}

        self.game = game
        self.screen = screen.copy()
        self.actionsize = 7
        self.sims = sims
        self.cpuct = 1
        self.EPS = 1e-8
    
    def reset(self):

        self.Qsa.clear()
        self.Nsa.clear()
        self.Ns.clear()
        self.Ps.clear()

        self.Es.clear()
        self.Vs.clear()

    def get_action_prop(self,temp=1):

        for i in range(self.sims):

            self.explore(self.game)

        board = self.game.board

        
        s = board.tostring()

        counts = [self.Nsa[(s,a)] if (s,a) in self.Nsa else 0 for a in range(self.actionsize)]

        if temp==0:
            bestA = np.argmax(counts)
            probs = [0]*len(counts)
            probs[bestA]=1
            return probs

        counts = [x**(1./temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [x/counts_sum for x in counts]
        return probs




    def explore(self,game):

        board = game.board
        vision = game.render_vision(self.screen)
        vision = vision.unsqueeze(0)
        vision = vision.float()
        s = board.tostring()
        
        # Checking to see if terminal node.  If it's a leaf node, the value is returned

        if s not in self.Es:

            if game.over==True:

                if game.tie==True:
                    return 0

                elif game.playerlist[game.turn].winner==True:
                    self.Es[s] = 1
                else:
                    self.Es[s] = -1
            else:
                self.Es[s] = 0

        if self.Es[s]!=0:
            return -self.Es[s]



        if s not in self.Ps:
            with torch.no_grad():
                output_pi, output_v = self.nnet.predict(vision)
                self.Ps[s],v = output_pi.numpy()[0], output_v.numpy()[0]


            valids = np.zeros((7))

            for c in range(self.actionsize):
                if game.valid_move(board,c)==True:
                    valids[c] = 1

            self.Ps[s] = self.Ps[s]*valids
            Total_Ps = np.sum(self.Ps[s])
            if Total_Ps > 0:
                self.Ps[s] /= Total_Ps
            else:
                print("All valid moves were masked, do workaround.")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Ns[s] = 1
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        for a in range(self.actionsize):
            if valids[a]:

                if (s,a) in self.Qsa:
                    u = self.Qsa[(s,a)] + self.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                else:
                    u = self.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s] + self.EPS)

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act

        next_game = copy.deepcopy(game)

        r = next_game.next_open_row(board,a)
        next_game.drop_piece(r,a,next_game.turn+1)
        if next_game.is_gameover(next_game.board,r,a,next_game.turn+1):
            next_game.playerlist[next_game.turn].winner = True
            next_game.over = True
        
        if next_game.is_tie(next_game.board):
            next_game.tie = True
            next_game.over = True

        next_game.turn = (next_game.turn + 1)%2

        v = self.explore(next_game)


        if (s,a) in self.Qsa:
            self.Qsa[(s,a)] = (self.Nsa[(s,a)]*self.Qsa[(s,a)] + v)/(self.Nsa[(s,a)]+1)
            self.Nsa[(s,a)] += 1


        else:
            self.Qsa[(s,a)] = v
            self.Nsa[(s,a)] = 1


        self.Ns[s] += 1



        return -v
