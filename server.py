'''
Brasília, 16/06/2019
Atualizações! Incluído suporte para UDP. Deu mais trabalho que eu pensava, mas ao
que parece está funcionando bem. Também incluí a questão da criação de uma lista
de listas para as salas - nesse caso falta estabelecer o serviço de salas de chat
em si, talvez incluindo os usuários a medida que forem entrando em endereços (ip, porta)
especificos de cada sala, talvez seja uma solução possível. Agora temos também um
feedback sobre o nome do usuário que envia as mensagens. Não sei se está 100%, talvez
uma melhoria seja incluir um modelo chave-valor - talvez uma hash table da vida - que
identifique unicamente um par (ip, porta) de conexão à uma string usada para apelido.
Fora isso, uma coisa que estava funcionando mas agora parou - não sei ainda o porque - é
o feedback, no server, de desconexão de usuários. Fora esse contratempo do feedback de
saída, acho que foram bons avanços.
'''

import socket
import time
import os
import sys

# definindo host e porta
host = '192.168.0.8'
port_tcp = 60000
port_udp = 61000
addr_tcp = (host, port_tcp)
addr_udp = (host, port_udp)

# instanciando lista de listas para salas. usando [] for _ in range nos
# garante listas filhas independentes
salas = [[] for _ in range(5)]

# instanciando lista de users
users = []

# instanciando objeto socket e fazendo a ligação dele com o host e a porta definidos
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Para fazer em máquinas diferentes, usar [socket.gethostname(), port] no bind
serversocket.bind(addr_tcp)

# o servidor suporta até 5 conexões simultâneas - temos que mudar para o nº de arquivos
# que o SO suporta. Uma vez que ele atinge o número máximo de conexões, o servidor para
# de responder / dar feedback sobre mensagens recebidas
serversocket.listen(5)
print("Conexão iniciada.")

try:
	while True:
		# aceita conexões. 
		(clientsocket, address) = serversocket.accept()

		# recebe nickname do cliente
		usuario = clientsocket.recv(1024)
		# converte mensagem (bytes -> str)
		str_user = str(usuario, 'utf-8')

		# recebe sala desejada
		sala = clientsocket.recv(1024)
		# converte mensagem (bytes -> str)
		int_sala = int(sala)

		# atualiza lista de usuários
		users.append((str_user, address))
		print(users)
		# atualiza lista de salas
		salas[int_sala].append(str_user)
		print(salas)
		
		#instanciando socket udp
		udpserversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# setando flag REUSEADDR para prevenir erros do tipo OSError: [Errno 98] Address already in use
		udpserversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# linkando socket a address
		udpserversocket.bind(addr_udp)

		# fork do interpretador Python. Agora, o processo que executa o disposto na linha
		# de comando do bash foi "copiado" em um processo filho idêntico - isso é necessário
		# para o suporte a múltiplos usuários simultaneamente
		pid = os.fork()

		# a chamada de sistema fork() retorna o ID do processo filho ao processo pai e 0 ao
		# processo filho. Com essa linha garantimos que utilizaremos o processo filho - ou
		# seja, que utilizaremos processos filhos diferentes a cada iteração
		if pid == 0:
			serversocket.close()
			#udpserversocket.close()
			print("Conectado com " + str_user, address)
			while True:
				# recebe mensagem. acho que o tamanho do buffer está ok
				msg, address_udp = udpserversocket.recvfrom(1024)
				if(msg == 'exit'):
					clientsocket.close()
					udpserversocket.close()
					sys.exit(0)
				if not msg: break
				str_msg = str(msg, 'utf-8')
				print(address_udp, str_user + ':' , str_msg)
			# quando o cliente se desconecta, mensagem indicativa e fechamento do socket
			# referente
			print("Finalizando conexão do cliente " + str_user, address)
			clientsocket.close()
			udpserversocket.close()
			sys.exit(0)
		else:
			clientsocket.close()
			udpserversocket.close()
except Exception as ex:
	template = "An exception of type {0} occurred. Arguments:\n{1!r}"
	message = template.format(type(ex).__name__, ex.args)
	print(message)