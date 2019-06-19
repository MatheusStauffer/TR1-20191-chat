'''
Brasília, 18/06/2019
Ajuste para uso de TCP apenas. Incluí feedback para o usuário que envia mensagem
recebê-la de volta também. Por enquanto, está parecendo mais um eco do que qualquer
outra coisa. O user escreve uma coisa e recebe o que escreveu logo abaixo. A ideia é
replicar o que aparece no server.py em cada instância de client.py que houver na sala.
Também adicionei um tratamento de entrada para o escolha de salas.
'''

import socket
import time

# definindo host e porta
host = 'localhost'
port_tcp = 60000
addr_tcp = (host, port_tcp)

# instanciando um objeto socket tcp e conectando com o host e porta definidos
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(addr_tcp)

# criando um alias para nickname
alias = input("Nickname: ")
# enviando nickname para servidor
clientsocket.sendto(alias.encode(), (addr_tcp))

usuario = clientsocket.recv(1024)
str_user = str(usuario, 'utf-8')

# pegando número de sala
sala = input("Digite a sala de chat que deseja entrar: ")

# tratamento de entrada para número de sala: verificando valor ascii correspondente
# a entrada dada
while True:
	if len(sala) > 1:
		sala = input("Digite um valor válido (1-5): ")
	elif(ord(sala) < 49 or ord(sala) > 54):
		sala = input("Digite um valor válido (1-5): ")
	else:
		break

# tratamento de entrada ainda por fazer
#while True:
#    if (int(sala) < 0 or int(sala) > 5):
#        break
#    else:
#		sala = input("Digite um valor válido: ")

# enviando número de sala para servidor
clientsocket.sendto(sala.encode(), (addr_tcp))

# pegando mensagem do teclado
message = input(alias + "-> ")

# loop: para finalizar a conexão - i.e., para sair do while, enviar 'q'.
# enquanto for enviada uma mensagem vazia, o laço pede impõe novamente
# a escrita - pela linha "message = input(alias + "-> ")"
while message != 'q':
	if message != '':
		clientsocket.sendto(message.encode(), (addr_tcp))
		print("Mensagem enviada.")
	msg = clientsocket.recv(1024)
	str_msg = str(msg, 'utf-8')
	print(str_user + ": " + str_msg)
	message = input(alias + "-> ")
	time.sleep(0.2)
clientsocket.close()