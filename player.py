import pygame as pg
import random as rd
from point import Point



class Player:
	img_bank = {}
	state_frames = {'stay': 3, 'run': 8}

	def __init__(self):
		self.health = 0
		
	
	def spawn(self, spawnpoints, frame_count):
		self.health = 20
		self.pos = Point(*rd.choice(spawnpoints))
		self.vel = Point(0, 0)
		self.state = 'stay', frame_count

		print('Respawned at', self.pos.getCoords())


	def intPos(self):
		return self.pos.getCoords(integer = True)


	def getImg(self, frame_count):
		state, key_frame = self.state
		mod = str(int((frame_count-key_frame)/150)%Player.state_frames[state])
		return Player.img_bank['player'][state + '_' + mod]
		