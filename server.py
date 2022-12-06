from jsonrpcserver import Success, method, serve, InvalidParams, Result, Error
import re, socket

server_port = 5001
queue = {}
games = {}

"""
This is the initial contact point for the clients, this function adds clients to the queue.
Servers sends 'waiting for players' -message when there are yet not enough players in the queue.
Server sends a 'ready to start' -message when 3 players have queued.
"""
@method
def want_to_play(player_ip): 
	global queue
	#check player is not in the queue already
	if player_ip in queue.values():
		return
	player_number = len(queue) + 1
	queue[player_number] = player_ip
	game_id = len(games) + 1
	if len(queue) >= 3:
		result = queue
		result['status'] = 'ready to start'
		result['game_id'] = game_id
		# Save players in games
		games[game_id] = queue
		queue = {}
	else:
		result = {}
		result['status'] = 'waiting for players'
		result['game_id'] = game_id
	return Success(result)
    
"""
This can be called if node want's to know if the peer connections are
started to establish. So if it needs to be worried about the other nodes statuses.
"""
@method
def is_connecting_started(game_id):
	result = {}
	if game_id in games.keys():
		result['connecting_started'] = True
		return Success(result)
	result['connecting_started'] = False
	return Success(result)

if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())
    serve(my_ip, server_port)