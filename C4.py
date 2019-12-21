import numpy as np
import pygame
import math
import sys
from C4Backend import Game, Player, Button, Menu_Piece, Cloud, Text_Editor, Key, Future
import time
import threading
import copy



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
white = (255,255,255)
red = (255,64,64)
yellow = (255,215,0)
orange = (255,97,3)
light_green = (127,255,0)
dark_green = (69,139,0)
brown = (139,69,19)
purple = (104,34,139)
pink = (255,110,180)
grey = (205,205,193)
cerulean = (0,229,238)

colorwheel = [
			cerulean
			,grey
			,red
			,yellow
			,orange
			,light_green
			,dark_green
			,brown
			,purple
			,pink
			]

small_colorwheel = [
	black
	,red
	,yellow
	]

keys = [
	Key(100,250,12,'RETURN',black,13)
	,Key(495,350,12,'->',black,275)
	,Key(471,350,12,'<-',black,276)
	,Key(470,250,12,'SPACE',black,32)
	,Key(100,350,12,'ESCAPE',black,27)
	]


screen = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load('Graphics/Background.png'),(display_width,int(display_height)))
table = pygame.transform.scale(pygame.image.load('Graphics/Table.png'),(display_width,int(display_height*0.5)))
namefont = pygame.font.SysFont('Comic Sans MS', 30)
clouds = []
text = Text_Editor('|')



def draw_text(screen,fontsize,x,y,text,color):
	font = pygame.font.SysFont('Comic Sans MS',fontsize)
	text = font.render(text,False,color)
	screen.blit(text,(x,y))

def lag(seconds):
	time.sleep(seconds)
	return True


buttons= [
	Button(218,525,20,'Start',black) #start_game
	,Button(100,100,55,'Player 1  ',black)
	,Button(500,100,55,'Player 2  ',black)
	,Button(100,200,25,'Simplemax',black)
	,Button(500,200,25,'Simplemax',black)
	,Button(100,250,25,'Simplemax',black)
	,Button(500,250,25,'Simplemax',black)
	,Button(100,300,25,'Simplemax',black)
	,Button(500,300,25,'Simplemax',black)
	,Button(100,350,25,'Simplemax',black)
	,Button(500,350,25,'Simplemax',black)
	,Button(100,400,25,'Simplemax',black)
	,Button(500,400,25,'Simplemax',black)
	,Button(77,450,14,'Medium',black)
	,Button(147,450,14,'Medium',black)
	,Button(217,450,14,'Medium',black)
	,Button(477,450,14,'Medium',black)
	,Button(547,450,14,'Medium',black)
	,Button(617,450,14,'Medium',black)
	,Button(293,525,20,'Controls',black)
	,Button(395,525,20,'Reset',black)
	,Button(473,525,20,'Quit Game',black)
	]


buttons[3].text = 'Human'
buttons[4].text = 'Human'
buttons[5].text = 'Random'
buttons[6].text = 'Random'
buttons[9].text = 'Minimax'
buttons[10].text = 'Minimax'
buttons[11].text = 'C4Net'
buttons[12].text = 'C4Net'
buttons[13].text = 'Easy'
buttons[15].text = 'Hard'
buttons[16].text = 'Easy'
buttons[18].text = 'Hard'
buttons[13].color = red
buttons[16].color = yellow
buttons[13].buttoncolor = black
buttons[16].buttoncolor = black

playertypes = [Menu_Piece(red,260,2),Menu_Piece(yellow,660,3)]
samplepiece = Menu_Piece(red,120,2)
samplepiece.y = 450


game = Game()



x = 3
y = 3

clouds.append(Cloud())



while game.over==False:


	for event in pygame.event.get():

		if event.type==pygame.QUIT:

			game.over = True









		if game.display=='Title':
			screen.fill((black))
			pygame.draw.rect(screen,blue,(3,3,795,595))

			mousex, mousey = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed()[0]


			draw_text(screen,64,175,0,'Connect Four',black)
			draw_text(screen,54,347,100,str(game.score[0]),game.player_colors[1])
			draw_text(screen,54,450,100,str(game.score[1]),game.player_colors[2])			


			for button in buttons:
				button.draw_button(screen,mousex,mousey)


			if buttons[0].got_pressed(click,mousex,mousey)==True:
				game.display = 'Game'

			if buttons[1].got_pressed(click,mousex,mousey)==True:
				game.display = 'Text Editor'
				game.editor = 1


			if buttons[2].got_pressed(click,mousex,mousey)==True:
				game.display = 'Text Editor'
				game.editor = 2


			if buttons[3].got_pressed(click,mousex,mousey)==True:
				game.playerlist[0].human = True
				game.playerlist[0].model = 'Human'
				if buttons[1].customized==False:
					game.playerlist[0].name = 'Player 1'
					buttons[1].text = 'Player 1'
				playertypes[0].y = buttons[3].y + 18


			if buttons[4].got_pressed(click,mousex,mousey)==True:
				game.playerlist[1].human = True
				game.playerlist[1].model = 'Human'
				if buttons[2].customized==False:
					game.playerlist[1].name = 'Player 2'
					buttons[2].text = 'Player 2'
				playertypes[1].y = buttons[4].y + 18


			if buttons[5].got_pressed(click,mousex,mousey)==True:
				game.playerlist[0].human = False
				game.playerlist[0].model = 'Random'
				if buttons[1].customized==False:
					game.playerlist[0].name = 'Jar Jar'
					buttons[1].text = 'Jar Jar'
				playertypes[0].y = buttons[5].y + 18


			if buttons[6].got_pressed(click,mousex,mousey)==True:
				game.playerlist[1].human = False
				game.playerlist[1].model = 'Random'
				if buttons[2].customized==False:
					game.playerlist[1].name = 'Jar Jar'
					buttons[2].text = 'Jar Jar'
				playertypes[1].y = buttons[6].y + 18


			if buttons[7].got_pressed(click,mousex,mousey)==True:
				game.playerlist[0].human = False
				game.playerlist[0].model = 'Simplemax'
				if buttons[1].customized==False:	
					game.playerlist[0].name = 'Bup'
					buttons[1].text = 'Bup'
				playertypes[0].y = buttons[7].y + 18


			if buttons[8].got_pressed(click,mousex,mousey)==True:
				game.playerlist[1].human = False
				game.playerlist[1].model = 'Simplemax'
				if buttons[2].customized==False:
					game.playerlist[1].name = 'Bup'
					buttons[2].text = 'Bup'
				playertypes[1].y = buttons[8].y + 18

			if buttons[9].got_pressed(click,mousex,mousey)==True:
				game.playerlist[0].human = False
				game.playerlist[0].model = 'Minimax'
				if buttons[1].customized==False:
					game.playerlist[0].name = 'Bran'
					buttons[1].text = 'Bran'
				playertypes[0].y = buttons[9].y + 18


			if buttons[10].got_pressed(click,mousex,mousey)==True:
				game.playerlist[1].human = False
				game.playerlist[1].model = 'Minimax'
				if buttons[2].customized==False:
					game.playerlist[1].name = 'Bran'
					buttons[2].text = 'Bran'
				playertypes[1].y = buttons[10].y + 18



			if buttons[11].got_pressed(click,mousex,mousey)==True:
				game.playerlist[0].human = False
				game.playerlist[0].model = 'C4Net'
				if buttons[1].customized==False:
					game.playerlist[0].name = 'Lain'
					buttons[1].text = 'Lain'
				playertypes[0].y = buttons[11].y + 18


			if buttons[12].got_pressed(click,mousex,mousey)==True:
				game.playerlist[1].human = False
				game.playerlist[1].model = 'C4Net'
				if buttons[2].customized==False:
					game.playerlist[0].name = 'Lain'
					buttons[2].text = 'Lain'
				playertypes[1].y = buttons[12].y + 18

			if buttons[13].got_pressed(click,mousex,mousey)==True:
				game.playerlist[0].depth = 1
				buttons[13].color, buttons[13].buttoncolor = playertypes[0].color, black
				buttons[14].color, buttons[14].buttoncolor = black, white
				buttons[15].color, buttons[15].buttoncolor = black, white				

			if buttons[16].got_pressed(click,mousex,mousey)==True:
				game.playerlist[1].depth = 1
				buttons[16].color, buttons[16].buttoncolor = playertypes[1].color, black
				buttons[17].color, buttons[17].buttoncolor = black, white
				buttons[18].color, buttons[18].buttoncolor = black, white

			if buttons[14].got_pressed(click,mousex,mousey)==True:
				game.playerlist[0].depth = 3
				buttons[14].color, buttons[14].buttoncolor = playertypes[0].color, black
				buttons[13].color, buttons[13].buttoncolor = black, white
				buttons[15].color, buttons[15].buttoncolor = black, white				

			if buttons[17].got_pressed(click,mousex,mousey)==True:
				game.playerlist[1].depth = 3
				buttons[17].color, buttons[17].buttoncolor = playertypes[1].color, black
				buttons[16].color, buttons[16].buttoncolor = black, white
				buttons[18].color, buttons[18].buttoncolor = black, white

			if buttons[15].got_pressed(click,mousex,mousey)==True:
				game.playerlist[0].depth = 5
				buttons[15].color, buttons[15].buttoncolor = playertypes[0].color, black
				buttons[14].color, buttons[14].buttoncolor = black, white
				buttons[13].color, buttons[13].buttoncolor = black, white				

			if buttons[18].got_pressed(click,mousex,mousey)==True:
				game.playerlist[1].depth = 5
				buttons[18].color, buttons[18].buttoncolor = playertypes[1].color, black
				buttons[17].color, buttons[17].buttoncolor = black, white
				buttons[16].color, buttons[16].buttoncolor = black, white


			if buttons[19].got_pressed(click,mousex,mousey)==True:
				game.display = 'Controls'

			if buttons[20].got_pressed(click,mousex,mousey)==True:
				game.score = [0,0]
				buttons[1].buttoncolor = white
				buttons[2].buttoncolor = white

			if buttons[21].got_pressed(click,mousex,mousey)==True:
				game.over = True


			if playertypes[0].got_pressed(click,mousex,mousey)==True:
				if playertypes[0].colorwheel+1==playertypes[1].colorwheel:
					playertypes[0].colorwheel = (playertypes[0].colorwheel + 2)%len(colorwheel)
				else:
					playertypes[0].colorwheel = (playertypes[0].colorwheel + 1)%len(colorwheel)
				newcolor = colorwheel[playertypes[0].colorwheel%len(colorwheel)]	
				playertypes[0].color = newcolor
				if buttons[1].buttoncolor!=black:
					buttons[1].buttoncolor = newcolor
				if game.playerlist[0].depth==1:
					buttons[13].color, buttons[13].buttoncolor = newcolor, black
				elif game.playerlist[0].depth==3:
					buttons[14].color, buttons[14].buttoncolor = newcolor, black
				elif game.playerlist[0].depth==5:
					buttons[15].color, buttons[15].buttoncolor = newcolor, black
				game.player_colors[1] = newcolor					


			if playertypes[1].got_pressed(click,mousex,mousey)==True:
				if playertypes[1].colorwheel+1==playertypes[0].colorwheel:
					playertypes[1].colorwheel = (playertypes[1].colorwheel + 2)%len(colorwheel)
				else:
					playertypes[1].colorwheel = (playertypes[1].colorwheel + 1)%len(colorwheel)
				newcolor = colorwheel[playertypes[1].colorwheel]
				playertypes[1].color = newcolor
				if buttons[2].buttoncolor!=black:
					buttons[2].buttoncolor = newcolor
				if game.playerlist[1].depth==1:
					buttons[16].color, buttons[16].buttoncolor = newcolor, black						
				elif game.playerlist[1].depth==3:
					buttons[17].color, buttons[17].buttoncolor = newcolor, black
				elif game.playerlist[1].depth==5:
					buttons[18].color, buttons[18].buttoncolor = newcolor, black						
				game.player_colors[2] = newcolor				



			playertypes[0].draw(screen)
			playertypes[1].draw(screen)



			pygame.display.flip()








		elif game.display=='Text Editor': 
			screen.fill((black))
			pygame.draw.rect(screen,blue,(3,3,795,595))

			
			if game.editingtext==False:
				game.editingtext = True
				tempname = text.create_string()



			if event.type==pygame.KEYDOWN:

				if event.key==pygame.K_BACKSPACE:
					tempname = text.delete_letter(tempname)

				elif event.key==pygame.K_LEFT:
					tempname = text.move_left(tempname)

				elif event.key==pygame.K_RIGHT:
					tempname = text.move_right(tempname)

				elif event.key==pygame.K_ESCAPE:
					game.display = 'Title'
					game.editingtext = False


				elif event.key==13:
					x = tempname.index('|')
					y = sorted(set(tempname))
					if tempname=='|' or (y[0]==' ' and y[1]=='|'):
						game.display = 'Title'
						game.editingtext = False
					elif game.editor==1:
						game.playerlist[0].name = tempname[:x] + tempname[x+1:]
						buttons[1].text = tempname[:x] + tempname[x+1:]
						buttons[1].customized = True
					elif game.editor==2:	
						game.playerlist[1].name = tempname[:x] + tempname[x+1:]
						buttons[2].text = tempname[:x] + tempname[x+1:]
						buttons[2].customized = True
					game.display = 'Title'
					game.editingtext = False


				elif event.key==pygame.K_SPACE:
					tempname = text.add_letter(tempname,' ')




				elif event.key==pygame.K_a and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'A')
				elif event.key==pygame.K_a:
					tempname = text.add_letter(tempname,'a')

				elif event.key==pygame.K_b and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'B')
				elif event.key==pygame.K_b:
					tempname = text.add_letter(tempname,'b')

				elif event.key==pygame.K_c and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'C')
				elif event.key==pygame.K_c:
					tempname = text.add_letter(tempname,'c')

				elif event.key==pygame.K_d and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'D')
				elif event.key==pygame.K_d:
					tempname = text.add_letter(tempname,'d')					

				elif event.key==pygame.K_e and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'E')
				elif event.key==pygame.K_e:
					tempname = text.add_letter(tempname,'e')

				elif event.key==pygame.K_f and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'F')
				elif event.key==pygame.K_f:
					tempname = text.add_letter(tempname,'f')


				elif event.key==pygame.K_g and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'G')
				elif event.key==pygame.K_g:
					tempname = text.add_letter(tempname,'g')


				elif event.key==pygame.K_h and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'H')
				elif event.key==pygame.K_h:
					tempname = text.add_letter(tempname,'h')


				elif event.key==pygame.K_i and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'I')
				elif event.key==pygame.K_i:
					tempname = text.add_letter(tempname,'i')


				elif event.key==pygame.K_j and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'J')
				elif event.key==pygame.K_j:
					tempname = text.add_letter(tempname,'j')


				elif event.key==pygame.K_k and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'K')
				elif event.key==pygame.K_k:
					tempname = text.add_letter(tempname,'k')


				elif event.key==pygame.K_l and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'L')
				elif event.key==pygame.K_l:
					tempname = text.add_letter(tempname,'l')


				elif event.key==pygame.K_m and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'M')
				elif event.key==pygame.K_m:
					tempname = text.add_letter(tempname,'m')


				elif event.key==pygame.K_n and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'N')
				elif event.key==pygame.K_n:
					tempname = text.add_letter(tempname,'n')


				elif event.key==pygame.K_o and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'O')
				elif event.key==pygame.K_o:
					tempname = text.add_letter(tempname,'o')


				elif event.key==pygame.K_p and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'P')
				elif event.key==pygame.K_p:
					tempname = text.add_letter(tempname,'p')


				elif event.key==pygame.K_q and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'Q')
				elif event.key==pygame.K_q:
					tempname = text.add_letter(tempname,'q')


				elif event.key==pygame.K_r and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'R')
				elif event.key==pygame.K_r:
					tempname = text.add_letter(tempname,'r')


				elif event.key==pygame.K_s and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'S')
				elif event.key==pygame.K_s:
					tempname = text.add_letter(tempname,'s')


				elif event.key==pygame.K_t and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'T')
				elif event.key==pygame.K_t:
					tempname = text.add_letter(tempname,'t')


				elif event.key==pygame.K_u and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'U')
				elif event.key==pygame.K_u:
					tempname = text.add_letter(tempname,'u')


				elif event.key==pygame.K_v and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'V')
				elif event.key==pygame.K_v:
					tempname = text.add_letter(tempname,'v')


				elif event.key==pygame.K_w and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'W')
				elif event.key==pygame.K_w:
					tempname = text.add_letter(tempname,'w')


				elif event.key==pygame.K_x and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'X')
				elif event.key==pygame.K_x:
					tempname = text.add_letter(tempname,'x')


				elif event.key==pygame.K_y and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'Y')
				elif event.key==pygame.K_y:
					tempname = text.add_letter(tempname,'y')


				elif event.key==pygame.K_z and (pygame.key.get_pressed()[pygame.K_LSHIFT]==True or pygame.key.get_pressed()[pygame.K_RSHIFT]==True):
					tempname = text.add_letter(tempname,'Z')
				elif event.key==pygame.K_z:
					tempname = text.add_letter(tempname,'z')


				elif event.key==pygame.K_0:
					tempname = text.add_letter(tempname,'0')

				elif event.key==pygame.K_1:
					tempname = text.add_letter(tempname,'1')

				elif event.key==pygame.K_2:
					tempname = text.add_letter(tempname,'2')

				elif event.key==pygame.K_3:
					tempname = text.add_letter(tempname,'3')

				elif event.key==pygame.K_4:
					tempname = text.add_letter(tempname,'4')

				elif event.key==pygame.K_5:
					tempname = text.add_letter(tempname,'5')

				elif event.key==pygame.K_6:
					tempname = text.add_letter(tempname,'6')

				elif event.key==pygame.K_7:
					tempname = text.add_letter(tempname,'7')

				elif event.key==pygame.K_8:
					tempname = text.add_letter(tempname,'8')

				elif event.key==pygame.K_9:
					tempname = text.add_letter(tempname,'9')

			for r in reversed(range(int(math.sqrt(400**2 + 300**2))+2)):
				if r%2==0:
					pygame.draw.circle(screen,small_colorwheel[r%3],(400,300),r)


			draw_text(screen,64,222,100,'Text Editor',black)
			pygame.draw.rect(screen,black,(144,294,503,112))
			pygame.draw.rect(screen,yellow,(146,296,499,108))
			pygame.draw.rect(screen,red,(148,298,495,104))
			pygame.draw.rect(screen,black,(150,300,491,100))

			draw_text(screen,64,155,300,tempname,game.player_colors[game.editor])


			pygame.display.flip()






		elif game.display=='Controls':


			mousex, mousey = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed()[0]


			screen.fill((black))
			pygame.draw.rect(screen,blue,(3,3,795,595))
			pygame.draw.rect(screen,black,(48,98,704,454))
			pygame.draw.rect(screen,red,(50,100,330,450))
			pygame.draw.rect(screen,yellow,(420,100,330,450))

			draw_text(screen,64,275,0,'Controls',black)
			draw_text(screen,48,156,100,'Menu',black)
			draw_text(screen,48,503,100,'Ingame',black)
			draw_text(screen,16,180,247,'Confirm name change',black)
			draw_text(screen,16,180,347,'Return to main menu',black)
			draw_text(screen,16,180,430,'Click on piece to',black)
			draw_text(screen,16,180,447,"change player's color",black)
			draw_text(screen,16,550,247,'Drop piece',black)
			draw_text(screen,16,550,347,'Move piece left and right',black)






			if samplepiece.got_pressed(click,mousex,mousey):
				samplepiece.colorwheel = (samplepiece.colorwheel + 1)%len(colorwheel)
				samplepiece.color = colorwheel[samplepiece.colorwheel]



			samplepiece.draw(screen)


			if event.type==pygame.KEYDOWN:

				if event.key==13:
					keys[0].pressed = True

				if event.key==275:
					keys[1].pressed = True

				if event.key==276:
					keys[2].pressed = True

				if event.key==32:
					keys[3].pressed = True

				if event.key==27:
					keys[4].pressed = True

			if event.type==pygame.KEYUP:

				if event.key==13:
					keys[0].pressed = False

				if event.key==275:
					keys[1].pressed = False

				if event.key==276:
					keys[2].pressed = False

				if event.key==32:
					keys[3].pressed = False

				if event.key==27:
					keys[4].pressed = False
					game.display = 'Title'

			for key in keys:
				key.draw_key(screen)





			pygame.display.flip()







		elif game.display=='Game':

			# print(game.playerlist[game.turn].thinking)

			if np.random.randint(0,1000)==0:
				clouds.append(Cloud())



			screen.blit(background,(0,0))
			screen.blit(table,(0,int(display_height*0.55)))
			for cloud in clouds:
				cloud.move()
				if (cloud.x + cloud.width)<0:
					clouds.remove(cloud)
				cloud.draw(screen)





			if event.type==pygame.KEYDOWN:
				if event.key==27:
					game.turn = np.random.randint(0,2)
					game.board = np.zeros((6,7))
					game.display = 'Title'


			if game.playerlist[game.turn].human==False:
				if game.playerlist[game.turn].thinking[0]==False:
					game.playerlist[game.turn].thinking[0] = True
					AI_thinking = Future(game.determine_preference)


				if AI_thinking.isdone()==True:
					game.preferred_choice = AI_thinking()

					game.playerlist[game.turn].thinking[1] = True



				if game.playerlist[game.turn].thinking[1]==True:


					if game.playerlist[game.turn].thinking[2]==False:
						moving_piece = Future(lag,0.5)
						game.playerlist[game.turn].thinking[2] = True

					if moving_piece.isdone()==True:


						if x!=game.preferred_choice:
							if abs(game.preferred_choice - x)<abs(7-abs(game.preferred_choice - x)):
								x = (x + np.sign(game.preferred_choice - x))%7
								game.playerlist[game.turn].thinking[2] = False



							else:
								x = (x - np.sign(game.preferred_choice - x))%7
								game.playerlist[game.turn].thinking[2] = False



			            
						elif x==game.preferred_choice:
							game.playerlist[game.turn].thinking = [False,False,False]
							valid_row = game.next_open_row(game.board,game.preferred_choice)
							game.drop_piece(valid_row,game.preferred_choice,game.turn+1)
							pygame.draw.rect(screen,black,(board_x-1,board_y-1,NUM_COLS*SQUARE_SIZE+2,NUM_ROWS*SQUARE_SIZE+2))
							pygame.draw.rect(screen,blue,board_dim)					
							game.draw_board(screen)
							if game.is_gameover(game.board,valid_row,game.preferred_choice,game.turn+1)==True:
								draw_text(screen,50,250,0,f'{game.playerlist[game.turn].name} wins!',game.player_colors[game.turn+1])
								pygame.display.flip()
								time.sleep(3)
								if game.score[game.turn]==9:
									game.score = [0,0]
									buttons[game.turn+1].buttoncolor = game.player_colors[game.turn+1]
									buttons[((game.turn+1)%2)+1].buttoncolor = white
								else:
									game.score[game.turn] += 1
								game.board = np.zeros((6,7))
								game.turn = np.random.randint(0,2)
								game.display = 'Title'
								game.board = np.zeros((6,7))
								game.turn = np.random.randint(0,2)
								game.display = 'Title'
								x = 3
								game.preferred_choice = None
							elif game.is_tie(game.board)==True:
								game.tie = True
								draw_text(screen,50,250,0,'It was a tie',black)
								pygame.display.flip()
								time.sleep(3)
								game.board = np.zeros((6,7))
								game.turn = np.random.randint(0,2)
								game.display = 'Title'
								x = 3
								game.preferred_choice = None
							else:
								game.preferred_choice = None
								game.turn = (game.turn+1)%2


				




			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT and game.playerlist[game.turn].human==True:
					x = (x-1)%7
				elif event.key==pygame.K_RIGHT and game.playerlist[game.turn].human==True:
					x = (x+1)%7	
				elif event.key==pygame.K_SPACE and game.playerlist[game.turn].human==True:
					choice = x

					if game.valid_move(game.board,choice)==True:
						valid_row = game.next_open_row(game.board,choice)
						game.drop_piece(valid_row,choice,game.turn+1)
						pygame.draw.rect(screen,black,(board_x-1,board_y-1,NUM_COLS*SQUARE_SIZE+2,NUM_ROWS*SQUARE_SIZE+2))
						pygame.draw.rect(screen,blue,board_dim)
						game.draw_board(screen)
						if game.is_gameover(game.board,valid_row,choice,game.turn+1)==True:
							draw_text(screen,50,250,0,f'{game.playerlist[game.turn].name} wins!',game.player_colors[game.turn+1])
							pygame.display.flip()
							time.sleep(3)
							if game.score[game.turn]==9:
								game.score = [0,0]
								buttons[game.turn+1].buttoncolor = game.player_colors[game.turn+1]
								buttons[((game.turn+1)%2)+1].buttoncolor = white
							else:
								game.score[game.turn] += 1
							game.board = np.zeros((6,7))
							game.turn = np.random.randint(0,2)
							game.display = 'Title'
							x = 3
						elif game.is_tie(game.board)==True:
							game.tie = True
							draw_text(screen,50,250,0,'It was a tie',black)
							pygame.display.flip()
							time.sleep(4)
							game.board = np.zeros((6,7))
							game.turn = np.random.randint(0,2)
							game.display = 'Title'
							x = 3
						else:
							game.turn = (game.turn+1)%2
					else:
						continue



			if np.random.randint(0,1000)==0:
				clouds.append(Cloud())

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


	# print(game.playerlist[game.turn].thinking)

	clock.tick(20) 



pygame.quit()

quit()


