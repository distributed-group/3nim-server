from jsonrpcserver import Success, method, serve
from Logger import Logger
import socket

server_port = 5001
my_ip = socket.gethostbyname(socket.gethostname())
logger = Logger('log.txt', my_ip)

# SERVER MEMORY
queue = {}
game_id_for_queue = None # Initialized when first player appears
starting_games = {} # Games, which are started and players trying to connect each others
running_games = {} # Games, which have all players connected


"""
This is the initial contact point for the clients, this function adds clients to the queue.
Servers sends 'waiting for players' -message when there are yet not enough players in the queue.
Server sends a 'ready to start' -message when 3 players have queued.
"""
@method
def want_to_play(player_ip): 
	global queue, game_id_for_queue
	#check player is not in the queue already
	if len(queue) == 0:
		game_id_for_queue = len(starting_games) + len(running_games) + 1
	if player_ip not in queue.values():
		player_number = len(queue) + 1
		queue[player_number] = player_ip
	if len(queue) >= 3:
		result = queue
		result['status'] = 'ready to start'
		result['game_id'] = game_id_for_queue
		# Save players in games
		starting_games[game_id_for_queue] = queue
		queue = {}
	else:
		result = {}
		result['status'] = 'Waiting for players...'
		result['game_id'] = game_id_for_queue
	return Success(result)
    
"""
This can be called if node want's to know if the peer connections are
started to establish. So if it needs to be worried about the other nodes statuses.
"""
@method
def is_connecting_started(game_id):
	logger.write_log('server was asked if the peer connecting has started for game ' + str(game_id))
	result = {}
	if game_id in starting_games.keys():
		result['connecting_started'] = True
	else:
		result['connecting_started'] = False
	return Success(result)

"""
This can be called if node want's to know if all players are connected.
"""
@method
def are_we_connected(game_id):
	logger.write_log('server was asked if nodes are connected for game ' + str(game_id))
	result = {}
	if game_id in running_games.keys():
		result['connected'] = True
	else:	
		result['connected'] = False
	return Success(result)

"""
This is called when node informs the server that it is connected to two other peers.
When all three have informed, server marks the game to be started and running.
"""
@method
def connected_to_two(game_id, player_ip):
	if game_id in running_games.keys():
		logger.write_log('The game is already running, why do you want the server know that you have two peers? ' + player_ip)
	elif game_id in starting_games.keys():
		#Note that this player has two peers
		logger.write_log('Game ' + str(game_id) + ' found, server knows now this player ' + player_ip + ' has two peers.')
		starting_games[game_id][player_ip] = True
		# Then let's check if all players have two peers
		count_connected = 0
		for i in range(1,4):
			p_ip = starting_games[game_id][i]
			if p_ip in starting_games[game_id].keys() and starting_games[game_id][p_ip]:
				count_connected = count_connected + 1
		if count_connected == 3:
			logger.write_log('Everybody is connected, wonderful. Game id: ' + str(game_id))
			running_games[game_id] = starting_games[game_id]
			del starting_games[game_id]
	else:
		logger.write_log('Game no found! With id ' + str(game_id))
	return Success({'received': True})


if __name__ == "__main__":
    serve(my_ip, server_port)
