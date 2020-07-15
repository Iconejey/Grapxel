import pygame, time
from pygame.locals import *
from ctypes import windll

 
# On initialise pygame
pygame.init()
taille_fenetre = (350, 250)
fenetre_rect = pygame.Rect((0, 0), taille_fenetre)
screen_surface = pygame.display.set_mode(taille_fenetre)
time.sleep(2)
windll.shcore.SetProcessDpiAwareness(1)
 
BLEU_NUIT = (5, 5, 30)
VERT = (0, 255, 0)
JAUNE = (255, 255, 0)
 
timer = pygame.time.Clock()
 
joueur = pygame.Surface((13, 13))
joueur.fill(JAUNE)
# Position du joueur
x, y = 25, 100
# Vitesse du joueur
vx, vy = 0, 0
# Gravité vers le bas donc positive
GRAVITE = 2
 
mur = pygame.Surface((25, 25))
mur.fill(VERT)
 
niveau = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	]
 
def dessiner_niveau(surface, niveau):
	for j, ligne in enumerate(niveau):
		for i, case in enumerate(ligne):
			if case == 1:
				surface.blit(mur, (i*25, j*25))
 
def from_coord_to_grid(pos):
	x, y = pos
	i = max(0, int(x // 25))
	j = max(0, int(y // 25))
	return i, j
 
def get_neighbour_blocks(niveau, i_start, j_start):
	blocks = list()
	for j in range(j_start, j_start+2):
		for i in range(i_start, i_start+2):
			if niveau[j][i] == 1:
				topleft = i*25, j*25
				blocks.append(pygame.Rect((topleft), (25, 25)))
	return blocks
 
def bloque_sur_collision(niveau, old_pos, new_pos, vx, vy):
	old_rect = pygame.Rect(old_pos, (15, 15))
	new_rect = pygame.Rect(new_pos, (15, 15))
	i, j = from_coord_to_grid(new_pos)
	collide_later = list()
	blocks = get_neighbour_blocks(niveau, i, j)
	for block in blocks:
		if not new_rect.colliderect(block):
			continue
 
		dx_correction, dy_correction = compute_penetration(block, old_rect, new_rect)
		# Dans cette première phase, on n'ajuste que les pénétrations sur un
		# seul axe.
		if dx_correction == 0.0:
			new_rect.top += dy_correction
			vy = 0.0
		elif dy_correction == 0.0:
			new_rect.left += dx_correction
			vx = 0.0
		else:
			collide_later.append(block)
 
	# Deuxième phase. On teste à présent les distances de pénétrations pour
	# les blocks qui en possédaient sur les 2 axes.
	for block in collide_later:
		dx_correction, dy_correction = compute_penetration(block, old_rect, new_rect)
		if dx_correction == dy_correction == 0.0:
			# Finalement plus de pénétration. Le new_rect a bougé précédemment
			# lors d'une résolution de collision
			continue
		if abs(dx_correction) < abs(dy_correction):
			# Faire la correction que sur l'axe X (plus bas)
			dy_correction = 0.0
		elif abs(dy_correction) < abs(dx_correction):
			# Faire la correction que sur l'axe Y (plus bas)
			dx_correction = 0.0
		if dy_correction != 0.0:
			new_rect.top += dy_correction
			vy = 0.0
		elif dx_correction != 0.0:
			new_rect.left += dx_correction
			vx = 0.0
 
	x, y = new_rect.topleft
	return x, y, vx, vy
 
def compute_penetration(block, old_rect, new_rect):
	dx_correction = dy_correction = 0.0
	if old_rect.bottom <= block.top < new_rect.bottom:
		dy_correction = block.top  - new_rect.bottom
	elif old_rect.top >= block.bottom > new_rect.top:
		dy_correction = block.bottom - new_rect.top

	if old_rect.right <= block.left < new_rect.right:
		dx_correction = block.left - new_rect.right
	elif old_rect.left >= block.right > new_rect.left:
		dx_correction = block.right - new_rect.left

	return dx_correction, dy_correction
 
# Boucle événementielle
continuer = True
while continuer:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = False
		elif event.type == KEYDOWN:
			if event.key == K_SPACE:
				vy = -20
 
	timer.tick(30)
	keys_pressed = pygame.key.get_pressed()
	# Sauvegarde de l'ancienne position
	old_x, old_y = x, y
	vx = (keys_pressed[K_RIGHT] - keys_pressed[K_LEFT]) * 5
	vy += GRAVITE
	vy = min(20, vy) # vy ne peut pas dépasser 25 sinon effet tunnel...
	x += vx
	y += vy
	x, y, vx, vy = bloque_sur_collision(niveau, (old_x, old_y), (x, y), vx, vy)
 
	screen_surface.fill(BLEU_NUIT)
	dessiner_niveau(screen_surface, niveau)
	screen_surface.blit(joueur, (x, y))
	pygame.display.flip()
 
pygame.quit()