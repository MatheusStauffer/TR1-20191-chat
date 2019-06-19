'''
Brasília, 18/06/2019
Ajuste para uso de TCP apenas. Incluí feedback para o usuário que envia mensagem
recebê-la de volta também usando a função sendto de socket. Faltam as salas em si.
'''

import socket
import time
import os
import sys

# definindo host e porta
host = 'localhost'
port_tcp = 60000
addr_tcp = (host, port_tcp)

# instanciando lista de listas para salas. usando [] for _ in range nos
# garante listas filhas independentes
salas = [[] for _ in range(5)]

# instanciando lista de users
users = []

# instanciando objeto socket TCP
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

		# enviando de volta ao cliente
		clientsocket.sendto(usuario, address)

		# recebe sala desejada
		sala = clientsocket.recv(1024)
		# converte mensagem (bytes -> str)
		int_sala = int(sala)

		# atualiza lista de usuários
		users.append((str_user, address))
		print(users)
		# atualiza lista de salas
		salas[int_sala-1].append(address)
		print(salas)
		
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
				msg = clientsocket.recv(1024)
				for address in salas[int_sala-1]:
					clientsocket.sendto(msg, address)
				if(msg == 'exit'):
					clientsocket.close()
					sys.exit(0)
				if not msg: break               
				str_msg = str(msg, 'utf-8')
				print(address, str_user + ':' , str_msg)
			# quando o cliente se desconecta, mensagem indicativa e fechamento do socket
			# respectivo
			print("Finalizando conexão do cliente " + str_user, address)
			clientsocket.close()
			sys.exit(0)
		else:
			clientsocket.close()
except Exception as ex:
	template = "An exception of type {0} occurred. Arguments:\n{1!r}"
	message = template.format(type(ex).__name__, ex.args)
	print(message)