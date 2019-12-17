from C4Backend import Game, Player
import numpy as np
import math

NUM_GAMES = 20
ITERATIONS = 25
NUM_MODELS = 20
normal_minimatrix = [1,2,5,1000]
PLAYERDEPTH = 3


games = [Game() for _ in range(NUM_MODELS)]


for game in games:
	for player in game.playerlist:
		player.model = 'Minimax'
		player.human = False
		for i in range(len(player.minimatrix)):
			player.minimatrix[i] = np.random.randint(-1000,1001)
		player.depth = PLAYERDEPTH
		
for j in range(ITERATIONS):
	print(j+1)
	for _ in range(NUM_GAMES):
		for game in games:
			starting_game_turn = game.turn
			while game.over==False:
				column = game.playerlist[game.turn].determine_preference(game.board,0,game.turn+1,game,game.playerlist[game.turn].minimatrix)
				row = game.next_open_row(game.board,column)
				game.board[row][column] = game.turn + 1
				if game.is_gameover(game.board,row,column,game.turn+1)==True:
					game.playerlist[game.turn].fitness += 2
					game.over = True
					game.turn = (starting_game_turn+1)%2
				elif game.is_tie(game.board)==True:
					for player in game.playerlist:
						player.fitness += 1
					game.over = True
					game.turn = (starting_game_turn+1)%2
				else:
					game.turn = (game.turn+1)%2
			game.over = False
			game.board = np.zeros((6,7))
	for game in games:
		for player in game.playerlist:
			for i in range(len(player.minimatrix)):
				player.minimatrix[i] = player.fitness * player.minimatrix[i]
			try:
				tempmatrix = np.stack([tempmatrix,np.array(player.minimatrix)],axis=0)
			except:
				tempmatrix = np.array(player.minimatrix)
			# print(f'{player.minimatrix} with fitness of {player.fitness}')
			player.fitness = 0
		try:
			finalmatrix = np.concatenate([finalmatrix,tempmatrix],axis=0)
		except:
			finalmatrix = np.array(tempmatrix)
	maximum = np.amax(np.array([abs(np.mean(finalmatrix[:,i]/1000)) for i in range(finalmatrix.shape[1])]))
	print(np.array([int(np.mean(finalmatrix[:,i])/maximum) for i in range(finalmatrix.shape[1])]))
	for i in range(len(player.minimatrix)):
		mean = np.mean(finalmatrix[:,i])
		for game in games:
			for player in game.playerlist:
				if j==(ITERATIONS-1):
					player.minimatrix[i] = int(mean/maximum)
				else:
					if i==len(player.minimatrix)-1 and np.random.randint(0,11)>int((10*j/ITERATIONS) + 5):
						player.minimatrix = [1,2,5,1000]
					elif np.random.randint(0,11)>int((2*j/ITERATIONS) + 8):
						player.minimatrix[i] = np.random.randint(-1000,1001)
					else:
						player.minimatrix[i] = max(min(int((mean + np.random.uniform(-1 * abs(mean)/math.sqrt(j+1),(abs(mean)+1)/math.sqrt(j+1)))/maximum),1000),-1000)
	del tempmatrix
	del finalmatrix
	print(' ')




player = Player('Test')

print(games[0].playerlist[0].minimatrix)
print(player.minimatrix)



