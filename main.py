import os, json, terrain as tr, pygame as pg, time
from player import Player
from ctypes import windll


if __name__ == "__main__":
	with open('world/world_settings.json') as f:
		world_set = json.load(f)

	with open('world/world.json') as f:
		json_world = json.load(f)

	img_bank = tr.getIMG('img')
	Player.img_bank = img_bank

	windll.shcore.SetProcessDpiAwareness(1)
	SCR_SIZE = [900, 560]
	SCREEN = pg.display.set_mode(SCR_SIZE)

	player = Player()

	world_size = [v*16 for v in tr.getWorldSize(json_world)]
	surfaces = {k: pg.Surface(world_size) for k in ['main', 'effects']}
	surfaces['effects'].set_colorkey([0]*3)
	for i in [0, 1, 2]:
		surfaces[f'layer_{i}'] = tr.getLayerImg(json_world, f'layer_{i}', img_bank)

	os.system('cls')
	
	last_count = 0
	game_end = False
	while not game_end:
		time.sleep(1/1000)
		if time.perf_counter() - last_count >= 1/60:
			frame_count = int(time.perf_counter() * 1000)
			last_count = time.perf_counter()

			for event in pg.event.get():
				if event.type == pg.QUIT:
					game_end = True

			if player.health <= 0:
				player.spawn(world_set['spawnpoints'], frame_count)
			else:
				player.move(pg.key.get_pressed(), world_set['hitboxes'], frame_count)

			surfaces['main'].fill([21, 24, 33])

			surfaces['main'].blit(surfaces['layer_0'], [0, 0])
			surfaces['main'].blit(surfaces['effects'], [0, 0])
			surfaces['main'].blit(player.getImg(frame_count), player.intPos())
			surfaces['main'].blit(surfaces['layer_1'], [0, 0])
			surfaces['main'].blit(surfaces['layer_2'], [0, 0])
			
			mx, my = pg.mouse.get_pos()
			px, py = player.intPos()
			SW, SH = SCR_SIZE
			cx = (-px-8)*5 + SW/2 - (mx - SW/2)/4
			cy = (-py-8)*5 + SH/2 - (my - SH/2)/4

			cam = [(c if c <= 0 else 0) for c in (cx, cy)]
			W, H = tr.getWorldSize(json_world)
			SCREEN.blit(pg.transform.scale(surfaces['main'], [W*80, H*80]), cam)

			pg.display.update()