import numpy as np
import pygame
import math
import sys
from ConnectFourBackend import Game,Player

pygame.init()


NUM_ROWS = 6
NUM_COLS = 7
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


screen = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load('Graphics/Background.png'),(display_width,int(display_height)))
table = pygame.transform.scale(pygame.image.load('Graphics/Table.png'),(display_width,int(display_height*0.5)))
namefont = pygame.font.SysFont('Comic Sans MS', 30)
clouds = []


class Cloud():
	def __init__(self):
		self.velocity = -1/3
		self.x = display_width + 50
		self.y = np.random.randint(-int(display_height/4),int(display_height*7/24))
		self.width = np.random.randint(int(display_width/8),int(display_width/2))
		self.height = np.random.randint(int(display_height/10),int(display_height/2) - self.y - 50)

	def move(self):
		self.x += self.velocity

	def draw(self,screen):
		cloud = pygame.transform.scale(pygame.image.load('Graphics/Cloud.png'),(self.width,self.height))
		screen.blit(cloud,(self.x,self.y))


game = Game()


game.playerlist[0].human = False
game.playerlist[1].human = False

x = 3
y = 3

clouds.append(Cloud())





while game.over==False:


	for event in pygame.event.get():

		if event.type==pygame.QUIT:

			game.over = True



		if game.playerlist[game.turn].human==False and pygame.time.get_ticks()>1000:

			while game.valid_move(game.preferred_choice)==False:
				game.preferred_choice = np.random.randint(0,7)
			if x!=game.preferred_choice:
				if np.random.randint(0,31)==1:
					if abs(game.preferred_choice - x)<abs(7-abs(game.preferred_choice - x)):
						x = (x + np.sign(game.preferred_choice - x))%7


					else:
						x = (x - np.sign(game.preferred_choice - x))%7


				
			elif x==game.preferred_choice:
				valid_row = game.next_open_row(game.preferred_choice)
				game.drop_piece(valid_row,game.preferred_choice)
				game.is_gameover(valid_row,game.preferred_choice)
				game.is_tie()
				if game.over==True and game.tie==False:
					print(game.playerlist[game.turn].name + ' wins!')
				elif game.over==True and game.tie==True:
					print('It was a tie')
				else:
					game.turn = (game.turn+1)%2
					if game.playerlist[game.turn].human==False:
						game.preferred_choice = np.random.randint(0,7)




		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_LEFT and game.playerlist[game.turn].human==True:
				x = (x-1)%7
			elif event.key==pygame.K_RIGHT and game.playerlist[game.turn].human==True:
				x = (x+1)%7	
			elif event.key==pygame.K_SPACE and game.playerlist[game.turn].human==True:
				choice = x

				if game.valid_move(choice)==True:
					valid_row = game.next_open_row(choice)
					game.drop_piece(valid_row,choice)
					game.is_gameover(valid_row,choice)
					game.is_tie()
					if game.over==True and game.tie==False:
						print(game.playerlist[game.turn].name + ' wins!')
					elif game.over==True and game.tie==True:
						print('It was a tie')
					else:
						game.turn = (game.turn+1)%2
						if game.playerlist[game.turn].human==False:
							game.preferred_choice = np.random.randint(0,7) 
				else:
					continue

		if event.type==pygame.KEYUP:
			if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_SPACE:
				x = x

	if np.random.randint(0,1000)==0:
		clouds.append(Cloud())



	screen.blit(background,(0,0))
	screen.blit(table,(0,int(display_height*0.55)))
	for cloud in clouds:
		cloud.move()
		if (cloud.x + cloud.width)<0:
			clouds.remove(cloud)
		cloud.draw(screen)
	pygame.draw.rect(screen,black,(board_x-1,board_y-1,NUM_COLS*SQUARE_SIZE+2,NUM_ROWS*SQUARE_SIZE+2))
	pygame.draw.rect(screen,blue,board_dim)
	game.draw_board(screen)


	if game.over==False:
		game.player_choice(screen,x,y)

	currentplayername = namefont.render(game.playerlist[game.turn].name, False, black)
	screen.blit(currentplayername,(15,0))

	pygame.display.flip()
	pygame.display.update()

	if pygame.event.peek().type==0:
		pygame.event.post(pygame.event.Event(4))

	clock.tick(60) 

	print(game.evaluate_board(game.board))


pygame.quit()

quit()


