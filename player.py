import pygame as pg
import random as rd



class Player:
	img_bank = {}
	state_frames = {'stay': 3, 'run': 8}

	def __init__(self):
		self.health = 0
		
	
	def spawn(self, spawnpoints, frame_count):
		self.health = 20
		self.pos = rd.choice(spawnpoints)
		self.vel = [0, 0]
		self.state = 'stay', frame_count

		print('Respawned at', self.pos)


	def intPos(self):
		return [int(v) for v in self.pos]


	def getImg(self, frame_count):
		state, key_frame = self.state
		mod = str(int((frame_count-key_frame)/150)%Player.state_frames[state])
		return Player.img_bank['player'][state + '_' + mod]
		