from jsonrpcserver import Success, method, serve, InvalidParams, Result, Error
import re, socket

queue = {}

@method
def want_to_play(player_ip): 
	global queue
	queue['player'+str(len(queue)+1)] = player_ip
	if len(queue) == 3:
		result = queue
		result['status'] = 'ready to start'
		queue = {}
	else:
		result = {'status':'wait for players'}
	return Success(result)
    
if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())
    serve(my_ip, 5001)
