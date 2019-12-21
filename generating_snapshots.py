import numpy as np
import pygame
import math
import sys
from C4Backend import Game, Player, Future
import time
import threading
import copy



pygame.init()


NUM_ROWS = 6
NUM_COLS = 7
ITERATIONS = 100
display_width = 800
display_height = 600
SQUARE_SIZE = 75
board_x = 137.5
board_y = 75
cloud_x = display_width
cloud_y = display_height/3
board_dim = (board_x,board_y,NUM_COLS*SQUARE_SIZE,NUM_ROWS*SQUARE_SIZE)
blue = (0,0,205)
black = (0,0,0)
red = (255,64,64)
yellow = (255,215,0)




screen = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load('Graphics/Background.png'),(display_width,int(display_height)))
table = pygame.transform.scale(pygame.image.load('Graphics/Table.png'),(display_width,int(display_height*0.5)))








game = Game()

for player in game.playerlist:
	player.depth = 3
	player.model = 'Random'
	player.human = False

x = 3
y = 3



for i in range(ITERATIONS):

	turn_counter = 1
	while game.over==False:


		for event in pygame.event.get():

			if event.type==pygame.QUIT:

				game.over = True



			screen.blit(background,(0,0))
			screen.blit(table,(0,int(display_height*0.55)))






			if game.playerlist[game.turn].human==False and game.over==False:
				if game.playerlist[game.turn].thinking[0]==False:
					game.playerlist[game.turn].thinking[0] = True
					AI_thinking = Future(game.determine_preference)

				if AI_thinking.isdone()==True:
					game.preferred_choice = AI_thinking()
					game.playerlist[game.turn].thinking[1] = True



				if game.playerlist[game.turn].thinking[1]==True:



					game.playerlist[game.turn].thinking = [False,False,False]
					valid_row = game.next_open_row(game.board,game.preferred_choice)
					game.drop_piece(valid_row,game.preferred_choice,game.turn+1)
					pygame.draw.rect(screen,black,(board_x-1,board_y-1,NUM_COLS*SQUARE_SIZE+2,NUM_ROWS*SQUARE_SIZE+2))
					pygame.draw.rect(screen,blue,board_dim)					
					game.draw_board(screen)


					rect = pygame.Rect(board_dim)
					sub = screen.subsurface(rect)
					pygame.image.save(sub, f"Snapshots/screenshot{i}_{turn_counter}.jpg")


					if game.is_gameover(game.board,valid_row,game.preferred_choice,game.turn+1)==True:
						game.board = np.zeros((6,7))
						game.turn = np.random.randint(0,2)
						game.preferred_choice = None
						game.over = True
					elif game.is_tie(game.board)==True:
						pygame.display.flip()
						game.board = np.zeros((6,7))
						game.turn = np.random.randint(0,2)
						game.over = True
					else:
						game.turn = (game.turn+1)%2


			pygame.draw.rect(screen,black,(board_x-1,board_y-1,NUM_COLS*SQUARE_SIZE+2,NUM_ROWS*SQUARE_SIZE+2))
			pygame.draw.rect(screen,blue,board_dim)
			game.draw_board(screen)


			pygame.display.flip()
			pygame.display.update()



			if pygame.event.peek().type==0:
				pygame.event.post(pygame.event.Event(4))



		clock.tick(20)
		turn_counter += 1

	turn_counter = 1
	game.over = False 



pygame.quit()

quit()


