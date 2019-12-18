import numpy as np
import pygame
import math
import sys
from C4Backend import Game, Player, Button, Menu_Piece, Cloud, Text_Editor, Key
import time
import copy
import threading


# http://code.activestate.com/recipes/84317/
# https://www.youtube.com/watch?v=09_LlHjoEiY


game_running = False
thinking = False


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



game = Game()


for player in game.playerlist:
	player.depth = 5
	player.model = 'Minimax'
	player.human = False

A = Future(game.playerlist[game.turn].determine_preference,game.board,0,game.turn+1,game)


# This doesn't work
while A.done==False:
	time.sleep(3)
	print('still waiting')


print(A())

# print(game.playerlist[game.turn].determine_preference(game.board,0,game.turn+1,game))










# def think():
# 	time.sleep(5)
# 	return 'done'


# while game_running==False:

# 	if thinking==False:
# 		thinking = True
# 		t1 = threading.Thread(target=think)
# 		t1.start()
# 		value = t1.join()
# 		game_running = True
# 		thinking = False

# print(value)
