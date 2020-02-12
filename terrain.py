import pygame as pg
import json, os, threading


def getIMG(path):
	d = {}
	for f in os.listdir(path):
		if len(f) > 4 and f[-4:] == '.png':
			d[f[:-4]] = pg.image.load(f'{path}/{f}')
		else:
			d[f] = getIMG(f'{path}/{f}')
	return d


def getWorldSize(json_world):
	return len(json_world['layer_0'][0]), len(json_world['layer_0'])


def getLayerImg(json_world, layer_key, img_bank):
	W, H = getWorldSize(json_world)

	surface = pg.Surface((W*16, H*16))
	surface.set_colorkey([29, 33, 45])
	surface.fill([29, 33, 45])

	surface2 = pg.Surface((W*16, H*16))
	surface2.fill([0]*3)
	
	for y in range(H):
		for x in range(W):
			case = json_world[layer_key][y][x]
			surface.blit(img_bank['world'][case], [x*16, y*16])

	surface2.blit(surface, [0, 0])
	surface2.set_colorkey([0]*3)
	return surface2


def getWorldImg(json_world, img_bank):
	W, H = getWorldSize(json_world)

	for layer in json_world:
		s = pg.Surface((W*16, H*16))
		s.fill([29, 33, 45])
		s.set_colorkey([29, 33, 45])
		s.blit(getLayerImg(json_world, layer, img_bank), [0, 0])
		yield s


def main():
	from ctypes import windll
	windll.shcore.SetProcessDpiAwareness(1)

	global tile, layer, world, map_img

	res = [960*3//2, 320*3//2]
	SCREEN = pg.display.set_mode(res)
	pg.display.set_caption('Grapxel')

	IMG = getIMG('img')
	with open('world/world.json') as f:
		world = json.load(f)

	W, H = getWorldSize(world)

	map_img = pg.Surface((W*16, H*16))
	map_img.fill([29, 33, 45])
	for s in getWorldImg(world, IMG):
		map_img.blit(s, [0, 0])

	os.system('cls')

	tile = 'dirt_2'
	layer = 'layer_1'
	done = False

	def input_loop():
		global tile, layer, world, map_img
		while not done:
			os.system('cls')
			print(layer, tile)
			inp = input().strip()

			if inp in IMG['world']:
				tile = inp

			if inp in world:
				layer = inp

			if inp == 'save':
				print('saving...')
				pg.image.save(map_img, 'map_img.png')
				with open('world/world.json', 'w') as f:
					f.write(json.dumps(world))

			if inp == 'clear':
				W, H = 60, 20
				world = {f'layer_{n}': [['empty' for i in range(W)] for i in range(H)] for n in range(3)}
				map_img = getWorldImg(world, IMG)

	input_thread = threading.Thread(target = input_loop)
	input_thread.start()

	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
				break
		if done:
			continue

		SCREEN.blit(pg.transform.smoothscale(map_img, res), [0, 0])

		mpos = [v*2//3 for v in pg.mouse.get_pos()]
		mcase = [int(v//16) for v in mpos]
		# print(*mpos, ':', *mcase, ' '*10, end = '\r')

		x, y = mcase
		if pg.mouse.get_pressed()[0] and world[layer][y][x] != tile and tile != 'hitbox':
			world[layer][y][x] = tile
			map_img.fill([29, 33, 45])
			for s in getWorldImg(world, IMG):
				map_img.blit(s, [0, 0])

		# pg.draw.rect(SCREEN, [128]*3, [v*3//2 for v in c for c in hitbox], 1)
		pg.draw.rect(SCREEN, [128]*3, [v*24 for v in mcase] + [24]*2, 1)

		pg.display.update()

	print('press [Enter] to quit.')
	input_thread.join()
	print('End')


if __name__ == '__main__':
	main()