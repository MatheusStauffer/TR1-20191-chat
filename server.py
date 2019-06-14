import socket
import time
import os
import sys

# definindo host e porta
host = '127.0.0.1'
port = 65000
addr = (host, port)

# pelo que eu entendi, a ideia do canal é ter um servidor que responda a múltiplos
# clientes simultaneamente - é o que fazemos aqui abaixo. Para enviar mensagens para
# destinatários específicos, a priori é só indicar seu host e porta acima - fazendo
# com que tenhamos uma conexão do tipo híbrida/P2P e não mais puramente cliente-servidor

# instanciando objeto socket e fazendo a ligação dele com o host e a porta definidos
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Para fazer em máquinas diferentes, usar [socket.gethostname(), port] no bind
serversocket.bind(addr)

# o servidor suporta até 5 conexões simultâneas - temos que mudar para o nº de arquivos
# que o SO suporta. Uma vez que ele atinge o número máximo de conexões, o servidor para
# de responder / dar feedback sobre mensagens recebidas
serversocket.listen(5)
print("Conexão iniciada.")

while True:
	# aceita conexões. 
	(clientsocket, address) = serversocket.accept()
	# fork do interpretador Python. Agora, o processo que executa o disposto na linha
	# de comando do bash foi "copiado" em um processo filho idêntico - isso é necessário
	# para o suporte a múltiplos usuários simultaneamente
	pid = os.fork()
	# a chamada de sistema fork() retorna o ID do processo filho ao processo pai e 0 ao
	# processo filho. Com essa linha garantimos que utilizaremos o processo filho - ou
	# seja, que utilizaremos processos filhos diferentes a cada iteração
	if pid == 0:
		serversocket.close()
		print("Conectado por ", address)
		while True:
			# recebe mensagem. acho que o tamanho do buffer está ok
			msg = clientsocket.recv(1024)
			if(msg == 'exit'):
				clientsocket.close()
				sys.exit(0)
			if not msg: break
			str_msg = str(msg, 'utf-8')
			print(address, str_msg)
		# quando o cliente se desconecta, mensagem indicativa e fechamento do socket
		# referente
		print("Finalizando conexão do cliente", address)
		clientsocket.close()
		sys.exit(0)
	else:
		clientsocket.close()