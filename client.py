'''
Brasília, 16/06/2019
Atualizações! Incluído suporte a UDP no envio de mensagens. Outros pontos interessantes
também, mais detalhes no arquivo server.py. Aqui ainda falta ajustar o tratamento de
entrada do usuário do número de sala.
'''

import socket
import time

# definindo host e porta
host = '192.168.0.8'
port_tcp = 60000
port_udp = 61000
addr_tcp = (host, port_tcp)
addr_udp = (host, port_udp)

# instanciando um objeto socket tcp e conectando com o host e porta definidos
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(addr_tcp)

# instanciando objeto socket udp
udpclientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# criando um alias para nickname
alias = input("Nickname: ")
# enviando nickname para servidor
clientsocket.sendto(alias.encode(), (addr_tcp))

# pegando número de sala
sala = input("Digite a sala de chat que deseja entrar: ")

# tratamento de entrada ainda por fazer
#while not isinstance(sala, int) or (sala < 0 or sala > 5):
#	sala = input("Informe um número de sala válido (inteiro 0-5): ")

# enviando número de sala para servidor
clientsocket.sendto(sala.encode(), (addr_tcp))

# pegando mensagem do teclado
message = input(alias + "-> ")

# loop: para finalizar a conexão - i.e., para sair do while, enviar 'q'.
# enquanto for enviada uma mensagem vazia, o laço pede impõe novamente
# a escrita - pela linha "message = input(alias + "-> ")"
while message != 'q':
	if message != '':
		udpclientsocket.sendto(message.encode(), (addr_udp))
		print("Mensagem enviada.")
	message = input(alias + "-> ")
	time.sleep(0.2)
clientsocket.close()