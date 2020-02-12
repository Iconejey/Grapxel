import socket, json, time, os
import threading as thrd
import random as rd

def tick(game, settings):
	for t in game['players']:
		for p in game['players'][t]:
			p = game['players'][t][p]
			if p['hp'] <= 0:
				p['vel'] = [0, 0]
				p['weapon'] = None
				p['hp'] = settings['max_hp']

				p['pos'] = game['map']['settings']["spawnpoints"][t][game['spawn_states'][t]]
				game['spawn_states'][t] += 1

				if game['spawn_states'][t] is 8:
					game['spawn_states'][t] = 0


def send_game(game):
	for t in game['players']:
		for p in game['players'][t]:
			game['players'][t][p]['sock'].send(game)


if __name__ == '__main__':
	with open('settings.json') as f:
		settings = json.load(f)

	game = {'players': {}, 'spawn_states': {'red': 0, 'blue': 0}}

	server_socket = socket.socket()
	server_socket.bind((socket.gethostname(), settings['port']))
	server_socket.settimeout(0.1)
	server_socket.listen(5)

	done = False

	# loops until all players connected
	def connection_loop():
		while len(game['players']) is not 8 and not done:
			print('Waiting for connection..', end = '\r')
			try:
				player_socket, (ip, port) = server_socket.accept()
				ID = ('%3s'%bin(len(game['players']))[2:]).replace(' ', '0')
				player_socket.send(ID.encode('ascii'))
				name = player_socket.recv(32).decode('ascii')

				game['players'][ID] = { 'name': name, 'pos': [0, 0], 'vel': [0, 0], 'hp': 0, 'weapon': None, 'sock': player_socket}

				print(ip, 'connected as', game['players'][ID]['name'], ID)

			except socket.timeout:
				pass

		input('End of connections. Press [Return].')

	os.system('cls')
	connection_thread = thrd.Thread(target = connection_loop)
	connection_thread.start()

	while not done:
		input()
		if len(game['players']) < 2:
			print('Not enough players.')
		else:
			done = True
			
	connection_thread.join()
	print('initialisation..')

	l = sorted(game['players'])
	rd.shuffle(l)
	game['players'] = {
		'red': {k: game['players'][k] for k in l[:len(l)//2]},
		'blue': {k: game['players'][k] for k in l[len(l)//2:]}
	}

	del l
	os.system('cls')

	for t in ['red', 'blue']:
		print(f'Team {t}:')
		for ID, player in game['players'][t].items():
			print(player['name'])
		print()

	# print(game)

	with open('world/world.json') as f:
		game['map'] = json.load(f)

	with open('world/world_settings.json') as f:
		game['map']['settings'] = json.load(f)

	rd.shuffle(game['map']['settings']["spawnpoints"]["blue"])
	rd.shuffle(game['map']['settings']["spawnpoints"]["red"])

	tick(game, settings)


	def compute_loop():
		while game_state:
			tick(game, settings)


	def server_loop():
		while game_state:
			send_game(game)


	game_state = 1

	compute_thread = thrd.Thread(target = compute_loop)
	server_thread = thrd.Thread(target = server_loop)

	# compute_thread.start()
	# server_thread.start()