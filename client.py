import time, os, terrain, json, socket
from PIL import Image, ImageDraw
import pygame as pg
import random as rd

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


def connect(port):
	local_ip = socket.gethostbyname(socket.gethostname())
	network = '.'.join(local_ip.split('.')[:-1]) + '.'

	for n in range(1, 256):
		addr = network + str(n)
		s = socket.socket()
		s.settimeout(0.01)
		if not s.connect_ex((addr, port)):
			s.settimeout(1)
			print(addr, socket.getfqdn(addr).split('.')[0])
			return s


def main(self):
	H, W = SIZE = 160, 100
	PSCALE = 5
	BIG_SIZE = H*PSCALE, W*PSCALE

	SCREEN = pg.display.set_mode(BIG_SIZE)
	pg.display.set_caption('Grapxel')

	EFFECT_SURFACE = pg.Surface(SIZE)
	EFFECT_SURFACE.set_colorkey([0]*3)
	EFFECT_SURFACE.set_alpha(192)

	IMG = terrain.getIMG('img')
	bg_color = 29, 33, 45

	GAME_LOOP = True
	while GAME_LOOP:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				GAME_LOOP = False
				break

		if not GAME_LOOP:
			continue

		SCREEN.fill(bg_color)

		mpos = [c//PSCALE for c in pg.mouse.get_pos()]
		r = 4

		for y in range(H):
			for x in range(W):
				if rd.random() < 1/2:
					EFFECT_SURFACE.set_at([y, x], [0]*3)
		
		pg.draw.circle(EFFECT_SURFACE, [255]*3, mpos, 2)

		SCREEN.blit(pg.transform.scale(EFFECT_SURFACE, BIG_SIZE), (0, 0))

		pg.display.update()


if __name__ == '__main__':
	with open('settings.json') as f:
		settings = json.load(f)
	os.system('cls')
	name = input('Name: ').strip()
	print('Searching for server...')
	server_socket = connect(settings['port'])
	server_socket.send(name.encode('ascii'))
	ID = server_socket.recv(3).decode('ascii')
	print('connected as', name, ID, '\nWaiting for game to start...')