from jsonrpcserver import Success, method, serve, InvalidParams, Result, Error
import re, socket

server_port = 5001
queue = {}

"""
This is the initial contact point for the clients, this function adds clients to the queue.
Servers sends 'waiting for players' -message when there are yet not enough players in the queue.
Server sends a 'ready to start' -message when 3 players have queued.
"""
@method
def want_to_play(player_ip): 
	global queue
	player_number = len(queue) + 1
	queue[player_number] = player_ip
	if len(queue) >= 3:
		result = queue
		result['status'] = 'ready to start'
		queue = {}
	else:
		result = {}
		result['status'] = 'waiting for players'
	return Success(result)
    
if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())
    serve(my_ip, server_port)