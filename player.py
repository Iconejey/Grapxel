import pygame as pg, random as rd


class Player:
	img_bank = {}
	state_frames = {'jump': 1, 'stay': 4, 'run': 8}
	body_hitbox = [3, 3, 9, 13]

	def __init__(self):
		self.health = 0
		
	
	def spawn(self, spawnpoints, frame_count):
		self.health = 20
		self.pos = rd.choice(spawnpoints)
		self.vel = [0, 0]
		self.state = 'stay', frame_count
		self.look = 'right'

		print('Respawned at', self.pos)


	def intPos(self):
		return [int(v) for v in self.pos]


	def getImg(self, frame_count):
		state, key_frame = self.state
		mod = str(int((frame_count-key_frame)/100)%Player.state_frames[state])
		img = Player.img_bank['player'][state + '_' + mod]
		return pg.transform.flip(img, self.look == 'left', False)


	def move(self, keys, hitboxes, frame):
		speed_limit = 1

		# JUMP
		if keys[pg.K_SPACE] and self.vel[1] is 0:
			self.vel[1] -= 5

		# LEFT
		if keys[pg.K_a]:
			self.look = 'left'
			if self.state[0] == 'jump' and self.vel[0] > -speed_limit:
				self.vel[0] -= 0.1
				if self.vel[0] < -speed_limit:
					self.vel[0] = -speed_limit
			else:
				if self.state[0] != 'run':
					self.state = 'run', frame
				self.vel[0] = -3

		# RIGHT
		elif keys[pg.K_d]:
			self.look = 'right'
			if self.state[0] == 'jump' and self.vel[0] < speed_limit:
				self.vel[0] += 0.1
				if self.vel[0] > speed_limit:
					self.vel[0] = speed_limit
			else:
				if self.state[0] != 'run':
					self.state = 'run', frame
				self.vel[0] = 3

		elif self.state[0] == 'run':
			self.vel[0] = 0
			self.state = 'stay', frame

		self.vel[1] = min(self.vel[1] + .5, 10)

		old_pos = self.intPos()
		old_rect = pg.Rect([a + b for a, b in zip(old_pos + [0, 0], Player.body_hitbox)])

		for i in range(2):
			self.pos[i] += self.vel[i]

		new_pos = self.intPos()
		new_rect = pg.Rect([a + b for a, b in zip(new_pos + [0, 0], Player.body_hitbox)])

		for hitbox in hitboxes:
			hrect = pg.Rect(*hitbox)
			if hrect.colliderect(new_rect):
				dx = dy = 0
				
				if old_rect.y + old_rect.h <= hrect.y < new_rect.y + new_rect.h:
					dy = hrect.y  - (new_rect.y + new_rect.h)
				elif old_rect.y >= hrect.y + hrect.h > new_rect.y:
					dy = hrect.y + hrect.h - new_rect.y

				if old_rect.x + old_rect.w <= hrect.x < new_rect.x + new_rect.w:
					dx = hrect.x - (new_rect.x + new_rect.w)
				elif old_rect.x >= hrect.x + hrect.w > new_rect.x:
					dx = hrect.x + hrect.w - new_rect.x

				if not dx == dy == 0:
					if abs(dx) < abs(dy) and dx is not 0:
						dy = 0
					elif dy is not 0:
						dx = 0

					if dx is not 0:
						self.pos[0] += dx
						self.vel[0] = 0

					elif dy is not 0:
						self.pos[1] += dy
						self.vel[1] = 0